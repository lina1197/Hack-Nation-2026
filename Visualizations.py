import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from typing import Dict, Any, List


class HealthcareVisualizer:
    """Visualization tools for healthcare facility data."""
    
    def __init__(self, rag_system):
        """
        Initialize visualizer.
        
        Args:
            rag_system: DocumentRAG instance
        """
        self.rag = rag_system
        self.df = rag_system.df
        
    def create_facility_map(self, region: str = None, specialty: str = None) -> go.Figure:
        """
        Create an interactive map of facilities.
        
        Args:
            region: Filter by region
            specialty: Filter by specialty
            
        Returns:
            Plotly figure
        """
        # Filter data
        df_filtered = self.df.copy()
        
        if region:
            df_filtered = df_filtered[
                (df_filtered['address_stateOrRegion'].str.contains(region, case=False, na=False)) |
                (df_filtered['address_city'].str.contains(region, case=False, na=False))
            ]
        
        if specialty:
            def has_specialty(specialties_str):
                if pd.isna(specialties_str):
                    return False
                try:
                    specialties = json.loads(specialties_str) if isinstance(specialties_str, str) else specialties_str
                    return specialty.lower() in [s.lower() for s in specialties]
                except:
                    return False
            df_filtered = df_filtered[df_filtered['specialties'].apply(has_specialty)]
        
        # For Ghana, use approximate coordinates if not available
        # Note: In production, you'd geocode the addresses
        ghana_coords = {
            'Greater Accra': (5.6037, -0.1870),
            'Ashanti': (6.6885, -1.6244),
            'Western': (5.5500, -2.2500),
            'Central': (5.2500, -1.0000),
            'Eastern': (6.1500, -0.5000),
            'Volta': (6.5000, 0.5000),
            'Northern': (9.4000, -1.0000),
            'Upper East': (10.7500, -0.9000),
            'Upper West': (10.3000, -2.3000),
            'Bono': (7.6500, -2.5000),
        }
        
        # Add coordinates (simplified - would need geocoding in production)
        lats = []
        lons = []
        for _, row in df_filtered.iterrows():
            region_name = row.get('address_stateOrRegion', 'Greater Accra')
            if region_name in ghana_coords:
                lat, lon = ghana_coords[region_name]
                # Add small random offset to separate overlapping points
                import random
                lats.append(lat + random.uniform(-0.05, 0.05))
                lons.append(lon + random.uniform(-0.05, 0.05))
            else:
                lats.append(6.5244)  # Default to Kumasi
                lons.append(-1.6244)
        
        df_filtered['lat'] = lats
        df_filtered['lon'] = lons
        
        # Create hover text
        hover_texts = []
        for _, row in df_filtered.iterrows():
            try:
                specialties = json.loads(row['specialties']) if isinstance(row['specialties'], str) else row.get('specialties', [])
                specialty_str = ', '.join(specialties[:3]) if specialties else 'N/A'
            except:
                specialty_str = 'N/A'
                
            hover_text = f"""
            <b>{row.get('name', 'Unknown')}</b><br>
            Type: {row.get('facilityTypeId', 'N/A')}<br>
            Location: {row.get('address_city', 'N/A')}, {row.get('address_stateOrRegion', 'N/A')}<br>
            Specialties: {specialty_str}<br>
            Capacity: {row.get('capacity', 'N/A')} beds
            """
            hover_texts.append(hover_text)
        
        df_filtered['hover_text'] = hover_texts
        
        # Create map
        fig = go.Figure()
        
        # Add facility markers
        fig.add_trace(go.Scattermapbox(
            lat=df_filtered['lat'],
            lon=df_filtered['lon'],
            mode='markers',
            marker=dict(
                size=10,
                color='red',
                opacity=0.7
            ),
            text=df_filtered['hover_text'],
            hoverinfo='text',
            name='Facilities'
        ))
        
        # Update layout
        fig.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=7.9465, lon=-1.0232),  # Center on Ghana
                zoom=6
            ),
            title=f"Healthcare Facilities Map{f' - {region}' if region else ''}{f' - {specialty}' if specialty else ''}",
            height=600,
            showlegend=True
        )
        
        return fig
    
    def create_medical_desert_heatmap(self, specialty: str) -> go.Figure:
        """
        Create a heatmap showing medical desert severity by region.
        
        Args:
            specialty: Medical specialty to analyze
            
        Returns:
            Plotly figure
        """
        regions = self.df['address_stateOrRegion'].unique()
        regions = [r for r in regions if pd.notna(r)]
        
        desert_data = []
        for region in regions:
            analysis = self.rag.detect_medical_deserts(specialty, region)
            severity_map = {'none': 0, 'moderate': 1, 'severe': 2, 'critical': 3}
            desert_data.append({
                'region': region,
                'facilities': analysis.get('specialty_facilities', 0),
                'severity': severity_map.get(analysis.get('desert_severity', 'none'), 0),
                'severity_label': analysis.get('desert_severity', 'none')
            })
        
        df_desert = pd.DataFrame(desert_data)
        df_desert = df_desert.sort_values('severity', ascending=False)
        
        # Create bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_desert['region'],
            y=df_desert['facilities'],
            marker_color=['red' if s >= 2 else 'orange' if s == 1 else 'green' 
                          for s in df_desert['severity']],
            text=df_desert['severity_label'],
            hovertemplate='<b>%{x}</b><br>Facilities: %{y}<br>Severity: %{text}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'Medical Desert Analysis: {specialty} by Region',
            xaxis_title='Region',
            yaxis_title='Number of Facilities',
            height=500
        )
        
        return fig
    
    def create_specialty_distribution(self) -> go.Figure:
        """Create a chart showing specialty distribution across facilities."""
        specialty_counts = {}
        
        for _, row in self.df.iterrows():
            if pd.notna(row.get('specialties')):
                try:
                    specialties = json.loads(row['specialties']) if isinstance(row['specialties'], str) else row['specialties']
                    for specialty in specialties:
                        specialty_counts[specialty] = specialty_counts.get(specialty, 0) + 1
                except:
                    pass
        
        # Sort by count
        sorted_specialties = sorted(specialty_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Take top 20
        top_specialties = sorted_specialties[:20]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=[s[1] for s in top_specialties],
            y=[s[0] for s in top_specialties],
            orientation='h',
            marker_color='lightblue'
        ))
        
        fig.update_layout(
            title='Top 20 Medical Specialties Available in Ghana',
            xaxis_title='Number of Facilities',
            yaxis_title='Specialty',
            height=600
        )
        
        return fig
    
    def create_facility_type_pie(self) -> go.Figure:
        """Create a pie chart of facility types."""
        type_counts = self.df['facilityTypeId'].value_counts()
        
        fig = go.Figure()
        
        fig.add_trace(go.Pie(
            labels=type_counts.index,
            values=type_counts.values,
            hole=0.3
        ))
        
        fig.update_layout(
            title='Distribution of Facility Types',
            height=400
        )
        
        return fig
    
    def create_coverage_dashboard(self, specialty: str = None) -> Dict[str, go.Figure]:
        """
        Create a comprehensive dashboard of visualizations.
        
        Args:
            specialty: Optional specialty to focus on
            
        Returns:
            Dictionary of Plotly figures
        """
        dashboard = {}
        
        # Map
        dashboard['map'] = self.create_facility_map(specialty=specialty)
        
        # Desert heatmap
        if specialty:
            dashboard['desert_heatmap'] = self.create_medical_desert_heatmap(specialty)
        
        # Specialty distribution
        dashboard['specialty_distribution'] = self.create_specialty_distribution()
        
        # Facility types
        dashboard['facility_types'] = self.create_facility_type_pie()
        
        return dashboard