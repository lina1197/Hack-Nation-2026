import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import json
from sentence_transformers import SentenceTransformer
import faiss


class DocumentRAG:
    """RAG system for intelligent document parsing with citation tracking."""
    
    def __init__(self, csv_path: str, embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize the RAG system with the Virtue Foundation dataset.
        
        Args:
            csv_path: Path to the CSV dataset
            embedding_model: Name of the sentence transformer model to use
        """
        self.df = pd.read_csv(csv_path)
        self.embedding_model = SentenceTransformer(embedding_model)
        self.index = None
        self.document_chunks = []
        self.build_index()
        
    def build_index(self):
        """Build FAISS index from the dataset."""
        print("Building FAISS index...")
        
        # Create searchable text chunks from each facility/NGO record
        self.document_chunks = []
        embeddings_list = []
        
        for idx, row in self.df.iterrows():
            # Create comprehensive text representation
            text_parts = []
            
            # Basic info
            if pd.notna(row.get('name')):
                text_parts.append(f"Name: {row['name']}")
            
            # Specialties
            if pd.notna(row.get('specialties')):
                try:
                    specialties = json.loads(row['specialties']) if isinstance(row['specialties'], str) else row['specialties']
                    if specialties:
                        text_parts.append(f"Specialties: {', '.join(specialties)}")
                except:
                    pass
            
            # Procedures
            if pd.notna(row.get('procedure')):
                try:
                    procedures = json.loads(row['procedure']) if isinstance(row['procedure'], str) else row['procedure']
                    if procedures:
                        text_parts.append(f"Procedures: {'; '.join(procedures)}")
                except:
                    pass
            
            # Equipment
            if pd.notna(row.get('equipment')):
                try:
                    equipment = json.loads(row['equipment']) if isinstance(row['equipment'], str) else row['equipment']
                    if equipment:
                        text_parts.append(f"Equipment: {'; '.join(equipment)}")
                except:
                    pass
            
            # Capabilities
            if pd.notna(row.get('capability')):
                try:
                    capabilities = json.loads(row['capability']) if isinstance(row['capability'], str) else row['capability']
                    if capabilities:
                        text_parts.append(f"Capabilities: {'; '.join(capabilities)}")
                except:
                    pass
            
            # Location
            location_parts = []
            if pd.notna(row.get('address_city')):
                location_parts.append(row['address_city'])
            if pd.notna(row.get('address_stateOrRegion')):
                location_parts.append(row['address_stateOrRegion'])
            if pd.notna(row.get('address_country')):
                location_parts.append(row['address_country'])
            if location_parts:
                text_parts.append(f"Location: {', '.join(location_parts)}")
            
            # Facility type
            if pd.notna(row.get('facilityTypeId')):
                text_parts.append(f"Type: {row['facilityTypeId']}")
            
            # Combine all text
            chunk_text = " | ".join(text_parts)
            
            # Store chunk with metadata
            self.document_chunks.append({
                'text': chunk_text,
                'row_idx': idx,
                'name': row.get('name', 'Unknown'),
                'source_url': row.get('source_url', ''),
                'organization_type': row.get('organization_type', 'facility')
            })
            
            # Generate embedding
            embedding = self.embedding_model.encode(chunk_text)
            embeddings_list.append(embedding)
        
        # Build FAISS index
        embeddings_array = np.array(embeddings_list).astype('float32')
        dimension = embeddings_array.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings_array)
        
        print(f"Index built with {len(self.document_chunks)} documents")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant documents with citation information.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of search results with citations
        """
        # Encode query
        query_embedding = self.embedding_model.encode(query).astype('float32').reshape(1, -1)
        
        # Search
        distances, indices = self.index.search(query_embedding, top_k)
        
        # Prepare results with citations
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            chunk = self.document_chunks[idx]
            row_data = self.df.iloc[chunk['row_idx']].to_dict()
            
            results.append({
                'rank': i + 1,
                'distance': float(dist),
                'relevance_score': 1 / (1 + float(dist)),  # Convert distance to similarity score
                'text': chunk['text'],
                'name': chunk['name'],
                'source_url': chunk['source_url'],
                'row_idx': chunk['row_idx'],
                'organization_type': chunk['organization_type'],
                'full_data': row_data,
                'citation': {
                    'row': chunk['row_idx'],
                    'source': chunk['source_url'],
                    'name': chunk['name']
                }
            })
        
        return results
    
    def get_facility_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get facility/NGO data by exact name match."""
        matches = self.df[self.df['name'].str.lower() == name.lower()]
        if len(matches) > 0:
            return matches.iloc[0].to_dict()
        return None
    
    def get_facilities_by_region(self, region: str) -> pd.DataFrame:
        """Get all facilities in a specific region."""
        return self.df[
            (self.df['address_stateOrRegion'].str.contains(region, case=False, na=False)) |
            (self.df['address_city'].str.contains(region, case=False, na=False))
        ]
    
    def get_facilities_by_specialty(self, specialty: str) -> pd.DataFrame:
        """Get facilities offering a specific specialty."""
        def has_specialty(specialties_str):
            if pd.isna(specialties_str):
                return False
            try:
                specialties = json.loads(specialties_str) if isinstance(specialties_str, str) else specialties_str
                return specialty.lower() in [s.lower() for s in specialties]
            except:
                return False
        
        return self.df[self.df['specialties'].apply(has_specialty)]
    
    def detect_medical_deserts(self, specialty: str = None, region: str = None) -> Dict[str, Any]:
        """
        Detect medical deserts based on specialty and/or region.
        
        Args:
            specialty: Medical specialty to check for
            region: Geographic region to analyze
            
        Returns:
            Analysis of medical desert status with citations
        """
        analysis = {
            'specialty': specialty,
            'region': region,
            'total_facilities': len(self.df),
            'is_medical_desert': False,
            'desert_severity': 'none',
            'available_facilities': [],
            'citations': []
        }
        
        # Filter by region if specified
        if region:
            region_df = self.get_facilities_by_region(region)
            analysis['regional_facilities'] = len(region_df)
        else:
            region_df = self.df
        
        # Filter by specialty if specified
        if specialty:
            specialty_df = self.get_facilities_by_specialty(specialty)
            if region:
                specialty_df = specialty_df[
                    (specialty_df['address_stateOrRegion'].str.contains(region, case=False, na=False)) |
                    (specialty_df['address_city'].str.contains(region, case=False, na=False))
                ]
            
            analysis['specialty_facilities'] = len(specialty_df)
            
            # Determine desert status
            if len(specialty_df) == 0:
                analysis['is_medical_desert'] = True
                analysis['desert_severity'] = 'critical'
            elif len(specialty_df) < 3:
                analysis['is_medical_desert'] = True
                analysis['desert_severity'] = 'severe'
            elif len(specialty_df) < 5:
                analysis['desert_severity'] = 'moderate'
            
            # Add facility details with citations
            for idx, row in specialty_df.iterrows():
                analysis['available_facilities'].append({
                    'name': row.get('name', 'Unknown'),
                    'location': f"{row.get('address_city', '')}, {row.get('address_stateOrRegion', '')}",
                    'row_idx': idx
                })
                analysis['citations'].append({
                    'row': idx,
                    'source': row.get('source_url', ''),
                    'name': row.get('name', 'Unknown')
                })
        
        return analysis
    
    def validate_facility_claims(self, facility_name: str) -> Dict[str, Any]:
        """
        Validate facility claims by checking for completeness and anomalies.
        
        Args:
            facility_name: Name of the facility to validate
            
        Returns:
            Validation report with suspicious claims highlighted
        """
        facility = self.get_facility_by_name(facility_name)
        
        if not facility:
            return {'error': 'Facility not found'}
        
        validation = {
            'facility_name': facility_name,
            'completeness_score': 0,
            'suspicious_claims': [],
            'missing_critical_fields': [],
            'data_quality_issues': [],
            'citation': {
                'row': self.df[self.df['name'] == facility_name].index[0],
                'source': facility.get('source_url', ''),
                'name': facility_name
            }
        }
        
        # Check critical fields
        critical_fields = ['address_country', 'address_city', 'facilityTypeId', 'specialties']
        filled_fields = 0
        total_fields = len(facility)
        
        for field in critical_fields:
            if pd.notna(facility.get(field)) and facility.get(field) not in ['', '[]', 'null']:
                filled_fields += 1
            else:
                validation['missing_critical_fields'].append(field)
        
        # Calculate completeness
        for value in facility.values():
            if pd.notna(value) and value not in ['', '[]', 'null']:
                filled_fields += 1
        
        validation['completeness_score'] = round((filled_fields / total_fields) * 100, 2)
        
        # Check for suspicious claims
        try:
            # Check capacity claims
            if pd.notna(facility.get('capacity')):
                capacity = facility['capacity']
                if capacity > 1000:
                    validation['suspicious_claims'].append(
                        f"Very high bed capacity claimed: {capacity} beds (unusual for most facilities)"
                    )
            
            # Check doctor count
            if pd.notna(facility.get('numberDoctors')):
                doctors = facility['numberDoctors']
                if doctors > 200:
                    validation['suspicious_claims'].append(
                        f"Very high doctor count: {doctors} doctors"
                    )
            
            # Check specialty count
            if pd.notna(facility.get('specialties')):
                specialties = json.loads(facility['specialties']) if isinstance(facility['specialties'], str) else facility['specialties']
                if len(specialties) > 15:
                    validation['suspicious_claims'].append(
                        f"Unusually broad specialty coverage: {len(specialties)} specialties"
                    )
        except Exception as e:
            validation['data_quality_issues'].append(f"Error parsing data: {str(e)}")
        
        return validation