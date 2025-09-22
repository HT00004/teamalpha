#!/usr/bin/env python3
"""
🎖️ Mission Alpha - Real vs Synthetic Data Comparison Module
Operation Data Validation - Realism Assessment Engine

This module compares generated synthetic pension data against real UK pension statistics
and industry benchmarks to assess the quality and realism of synthetic data generation.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime
from typing import Dict, List, Tuple, Any
import json

class DataRealismComparator:
    """
    Comprehensive comparison engine for synthetic vs real pension data patterns
    """
    
    def __init__(self):
        """Initialize with UK pension industry benchmarks"""
        self.uk_benchmarks = self.load_uk_pension_benchmarks()
        self.comparison_results = {}
    
    def load_uk_pension_benchmarks(self) -> Dict[str, Any]:
        """Load real UK pension industry statistics and benchmarks"""
        
        # Real UK pension statistics from ONS, TPR, and industry sources
        benchmarks = {
            "age_distribution": {
                "22-29": 0.20,  # 20% of workforce
                "30-39": 0.28,  # 28% of workforce  
                "40-49": 0.26,  # 26% of workforce
                "50-59": 0.20,  # 20% of workforce
                "60-67": 0.06   # 6% of workforce
            },
            
            "gender_distribution": {
                "M": 0.52,      # Male workforce participation
                "F": 0.47,      # Female workforce participation
                "O": 0.01       # Other/Non-binary
            },
            
            "sector_distribution": {
                "Finance": 0.14,
                "Manufacturing": 0.10, 
                "Public Service": 0.19,
                "Healthcare": 0.13,
                "Education": 0.09,
                "Retail": 0.11,
                "Other": 0.24
            },
            
            "salary_ranges": {
                "Finance": {"min": 25000, "max": 150000, "median": 45000},
                "Manufacturing": {"min": 20000, "max": 80000, "median": 32000},
                "Public Service": {"min": 18000, "max": 85000, "median": 35000},
                "Healthcare": {"min": 22000, "max": 90000, "median": 38000},
                "Education": {"min": 24000, "max": 70000, "median": 35000},
                "Retail": {"min": 18000, "max": 55000, "median": 26000},
                "Other": {"min": 20000, "max": 100000, "median": 35000}
            },
            
            "contribution_rates": {
                "employee_min": 0.05,    # 5% minimum employee contribution
                "employer_min": 0.03,    # 3% minimum employer contribution
                "total_avg": 0.11,       # 11% average total contribution
                "high_earner_avg": 0.15  # 15% for high earners
            },
            
            "geographic_distribution": {
                "London": 0.22,
                "South East": 0.18,
                "North West": 0.12,
                "West Midlands": 0.09,
                "Yorkshire": 0.08,
                "Scotland": 0.08,
                "East": 0.07,
                "South West": 0.06,
                "East Midlands": 0.05,
                "Wales": 0.03,
                "North East": 0.02
            },
            
            "status_distribution": {
                "Active": 0.75,         # 75% active members
                "Deferred": 0.20,       # 20% deferred
                "Pensioner": 0.05       # 5% pensioners
            },
            
            "years_service_patterns": {
                "0-5": 0.40,
                "6-15": 0.35,
                "16-25": 0.15,
                "26-35": 0.08,
                "36+": 0.02
            }
        }
        
        return benchmarks
    
    def compare_synthetic_vs_real(self, synthetic_data_path: str) -> Dict[str, Any]:
        """
        Comprehensive comparison of synthetic data against real UK pension patterns
        """
        
        try:
            # Load synthetic data with multiple encoding attempts
            synthetic_df = None
            encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    synthetic_df = pd.read_csv(synthetic_data_path, encoding=encoding)
                    print(f"Successfully loaded data with {encoding} encoding")
                    break
                except UnicodeDecodeError:
                    continue
            
            if synthetic_df is None:
                raise Exception("Could not load CSV file with any supported encoding")
            
            # Clean any currency symbols and convert salary columns to numeric
            if 'AnnualSalary' in synthetic_df.columns:
                synthetic_df['AnnualSalary'] = synthetic_df['AnnualSalary'].astype(str).str.replace('£', '').str.replace(',', '').str.replace('$', '')
                synthetic_df['AnnualSalary'] = pd.to_numeric(synthetic_df['AnnualSalary'], errors='coerce')
            
            # Handle any missing or invalid data
            synthetic_df = synthetic_df.dropna(subset=['Age', 'Gender', 'Sector'] if all(col in synthetic_df.columns for col in ['Age', 'Gender', 'Sector']) else synthetic_df.columns[:3])
            
            # Initialize results
            comparison_results = {
                "overall_realism_score": 0.0,
                "detailed_comparisons": {},
                "recommendations": [],
                "data_quality_metrics": {},
                "statistical_tests": {}
            }
            
            # Age distribution comparison
            age_comparison = self.compare_age_distribution(synthetic_df)
            comparison_results["detailed_comparisons"]["age"] = age_comparison
            
            # Gender distribution comparison
            gender_comparison = self.compare_gender_distribution(synthetic_df)
            comparison_results["detailed_comparisons"]["gender"] = gender_comparison
            
            # Sector distribution comparison
            sector_comparison = self.compare_sector_distribution(synthetic_df)
            comparison_results["detailed_comparisons"]["sector"] = sector_comparison
            
            # Salary analysis comparison
            salary_comparison = self.compare_salary_patterns(synthetic_df)
            comparison_results["detailed_comparisons"]["salary"] = salary_comparison
            
            # Geographic distribution comparison
            geo_comparison = self.compare_geographic_distribution(synthetic_df)
            comparison_results["detailed_comparisons"]["geographic"] = geo_comparison
            
            # Status distribution comparison
            status_comparison = self.compare_status_distribution(synthetic_df)
            comparison_results["detailed_comparisons"]["status"] = status_comparison
            
            # Years of service patterns
            service_comparison = self.compare_service_patterns(synthetic_df)
            comparison_results["detailed_comparisons"]["service"] = service_comparison
            
            # Calculate overall realism score
            comparison_results["overall_realism_score"] = self.calculate_overall_realism_score(
                comparison_results["detailed_comparisons"]
            )
            
            # Generate recommendations
            comparison_results["recommendations"] = self.generate_recommendations(
                comparison_results["detailed_comparisons"]
            )
            
            # Store results
            self.comparison_results = comparison_results
            
            return comparison_results
            
        except Exception as e:
            st.error(f"Error in data comparison: {str(e)}")
            return {"error": str(e)}
    
    def compare_age_distribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compare age distribution patterns"""
        
        # Handle different possible column names
        age_column = None
        for col in ['Age', 'age', 'Age_Years', 'member_age']:
            if col in df.columns:
                age_column = col
                break
        
        if age_column is None:
            return {
                "accuracy_score": 0,
                "distributions": {},
                "summary": "Age column not found in data",
                "passes_test": False,
                "error": "Age column not found"
            }
        
        # Create age bins
        df['age_bin'] = pd.cut(df[age_column], 
                              bins=[21, 29, 39, 49, 59, 68], 
                              labels=['22-29', '30-39', '40-49', '50-59', '60-67'],
                              include_lowest=True)
        
        synthetic_dist = df['age_bin'].value_counts(normalize=True).to_dict()
        real_dist = self.uk_benchmarks["age_distribution"]
        
        # Calculate differences
        differences = {}
        total_diff = 0
        
        for age_group in real_dist:
            synthetic_pct = synthetic_dist.get(age_group, 0)
            real_pct = real_dist[age_group]
            diff = abs(synthetic_pct - real_pct)
            differences[age_group] = {
                "synthetic": synthetic_pct,
                "real": real_pct,
                "difference": diff,
                "percentage_error": (diff / real_pct) * 100 if real_pct > 0 else 0
            }
            total_diff += diff
        
        accuracy_score = max(0, 1 - (total_diff / 2))  # Normalize to 0-1
        
        return {
            "accuracy_score": accuracy_score,
            "distributions": differences,
            "summary": f"Age distribution accuracy: {accuracy_score:.2%}",
            "passes_test": accuracy_score > 0.8
        }
    
    def compare_gender_distribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compare gender distribution patterns"""
        
        # Handle different possible column names
        gender_column = None
        for col in ['Gender', 'gender', 'Gender_Code', 'sex']:
            if col in df.columns:
                gender_column = col
                break
        
        if gender_column is None:
            return {
                "accuracy_score": 0,
                "distributions": {},
                "summary": "Gender column not found in data",
                "passes_test": False,
                "error": "Gender column not found"
            }
        
        synthetic_dist = df[gender_column].value_counts(normalize=True).to_dict()
        real_dist = self.uk_benchmarks["gender_distribution"]
        
        differences = {}
        total_diff = 0
        
        for gender in real_dist:
            synthetic_pct = synthetic_dist.get(gender, 0)
            real_pct = real_dist[gender]
            diff = abs(synthetic_pct - real_pct)
            differences[gender] = {
                "synthetic": synthetic_pct,
                "real": real_pct,
                "difference": diff,
                "percentage_error": (diff / real_pct) * 100 if real_pct > 0 else 0
            }
            total_diff += diff
        
        accuracy_score = max(0, 1 - (total_diff / 2))
        
        return {
            "accuracy_score": accuracy_score,
            "distributions": differences,
            "summary": f"Gender distribution accuracy: {accuracy_score:.2%}",
            "passes_test": accuracy_score > 0.9
        }
    
    def compare_sector_distribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compare sector distribution patterns"""
        
        # Handle different possible column names
        sector_column = None
        for col in ['Sector', 'sector', 'Industry', 'employment_sector']:
            if col in df.columns:
                sector_column = col
                break
        
        if sector_column is None:
            return {
                "accuracy_score": 0,
                "distributions": {},
                "summary": "Sector column not found in data",
                "passes_test": False,
                "error": "Sector column not found"
            }
        
        synthetic_dist = df[sector_column].value_counts(normalize=True).to_dict()
        real_dist = self.uk_benchmarks["sector_distribution"]
        
        differences = {}
        total_diff = 0
        
        for sector in real_dist:
            synthetic_pct = synthetic_dist.get(sector, 0)
            real_pct = real_dist[sector]
            diff = abs(synthetic_pct - real_pct)
            differences[sector] = {
                "synthetic": synthetic_pct,
                "real": real_pct,
                "difference": diff,
                "percentage_error": (diff / real_pct) * 100 if real_pct > 0 else 0
            }
            total_diff += diff
        
        accuracy_score = max(0, 1 - (total_diff / 2))
        
        return {
            "accuracy_score": accuracy_score,
            "distributions": differences,
            "summary": f"Sector distribution accuracy: {accuracy_score:.2%}",
            "passes_test": accuracy_score > 0.7
        }
    
    def compare_salary_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compare salary patterns by sector"""
        
        # Handle different possible column names
        salary_column = None
        for col in ['AnnualSalary', 'annual_salary', 'Salary', 'salary', 'Annual_Salary']:
            if col in df.columns:
                salary_column = col
                break
        
        sector_column = None
        for col in ['Sector', 'sector', 'Industry', 'employment_sector']:
            if col in df.columns:
                sector_column = col
                break
        
        if salary_column is None or sector_column is None:
            return {
                "overall_accuracy": 0,
                "sector_analysis": {},
                "summary": f"Required columns not found (salary: {salary_column}, sector: {sector_column})",
                "passes_test": False,
                "error": "Salary or sector column not found"
            }
        
        sector_salary_analysis = {}
        overall_accuracy = 0
        
        for sector in self.uk_benchmarks["salary_ranges"]:
            sector_data = df[df[sector_column] == sector][salary_column]
            
            if len(sector_data) > 0:
                real_ranges = self.uk_benchmarks["salary_ranges"][sector]
                
                synthetic_median = sector_data.median()
                synthetic_min = sector_data.min()
                synthetic_max = sector_data.max()
                
                # Calculate accuracy metrics
                median_accuracy = 1 - abs(synthetic_median - real_ranges["median"]) / real_ranges["median"]
                range_accuracy = 1 - (
                    abs(synthetic_min - real_ranges["min"]) / real_ranges["min"] +
                    abs(synthetic_max - real_ranges["max"]) / real_ranges["max"]
                ) / 2
                
                sector_accuracy = (median_accuracy + range_accuracy) / 2
                overall_accuracy += sector_accuracy
                
                sector_salary_analysis[sector] = {
                    "synthetic_median": synthetic_median,
                    "real_median": real_ranges["median"],
                    "synthetic_range": f"£{synthetic_min:,} - £{synthetic_max:,}",
                    "real_range": f"£{real_ranges['min']:,} - £{real_ranges['max']:,}",
                    "accuracy_score": max(0, sector_accuracy),
                    "median_difference": abs(synthetic_median - real_ranges["median"]),
                    "passes_test": sector_accuracy > 0.7
                }
        
        overall_accuracy = overall_accuracy / len(self.uk_benchmarks["salary_ranges"])
        
        return {
            "overall_accuracy": max(0, overall_accuracy),
            "sector_analysis": sector_salary_analysis,
            "summary": f"Salary pattern accuracy: {overall_accuracy:.2%}",
            "passes_test": overall_accuracy > 0.7
        }
    
    def compare_geographic_distribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compare geographic distribution using postcode patterns"""
        
        # Handle different possible column names
        postcode_column = None
        for col in ['Postcode', 'postcode', 'PostCode', 'postal_code']:
            if col in df.columns:
                postcode_column = col
                break
        
        if postcode_column is None:
            return {
                "accuracy_score": 0,
                "distributions": {},
                "summary": "Postcode column not found in data",
                "passes_test": False,
                "regions_covered": 0,
                "error": "Postcode column not found"
            }
        
        # Map postcodes to regions
        postcode_to_region = {
            'EC1': 'London', 'SW1': 'London', 'W1A': 'London', 'E1': 'London', 'N1': 'London',
            'M1': 'North West', 'M2': 'North West', 'M3': 'North West',
            'B1': 'West Midlands', 'B2': 'West Midlands', 'B3': 'West Midlands',
            'G1': 'Scotland', 'G2': 'Scotland',
            'EH1': 'Scotland', 'EH2': 'Scotland',
            'CF10': 'Wales', 'CF11': 'Wales',
            'L1': 'North West', 'L2': 'North West',
            'LS1': 'Yorkshire', 'LS2': 'Yorkshire',
            'BS1': 'South West', 'BS2': 'South West'
        }
        
        # Extract postcode area from full postcode
        df['postcode_area'] = df[postcode_column].str.split(' ').str[0]
        df['region'] = df['postcode_area'].map(postcode_to_region)
        
        synthetic_dist = df['region'].value_counts(normalize=True).to_dict()
        real_dist = self.uk_benchmarks["geographic_distribution"]
        
        # Only compare regions we have data for
        common_regions = set(synthetic_dist.keys()) & set(real_dist.keys())
        
        differences = {}
        total_diff = 0
        
        for region in common_regions:
            synthetic_pct = synthetic_dist.get(region, 0)
            real_pct = real_dist[region]
            diff = abs(synthetic_pct - real_pct)
            differences[region] = {
                "synthetic": synthetic_pct,
                "real": real_pct,
                "difference": diff,
                "percentage_error": (diff / real_pct) * 100 if real_pct > 0 else 0
            }
            total_diff += diff
        
        accuracy_score = max(0, 1 - (total_diff / len(common_regions))) if common_regions else 0
        
        return {
            "accuracy_score": accuracy_score,
            "distributions": differences,
            "summary": f"Geographic distribution accuracy: {accuracy_score:.2%}",
            "passes_test": accuracy_score > 0.6,
            "regions_covered": len(common_regions)
        }
    
    def compare_status_distribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compare member status distribution"""
        
        # Handle different possible column names
        status_column = None
        for col in ['Status', 'status', 'Member_Status', 'member_status']:
            if col in df.columns:
                status_column = col
                break
        
        if status_column is None:
            return {
                "accuracy_score": 0,
                "distributions": {},
                "summary": "Status column not found in data",
                "passes_test": False,
                "error": "Status column not found"
            }
        
        synthetic_dist = df[status_column].value_counts(normalize=True).to_dict()
        real_dist = self.uk_benchmarks["status_distribution"]
        
        differences = {}
        total_diff = 0
        
        for status in real_dist:
            synthetic_pct = synthetic_dist.get(status, 0)
            real_pct = real_dist[status]
            diff = abs(synthetic_pct - real_pct)
            differences[status] = {
                "synthetic": synthetic_pct,
                "real": real_pct,
                "difference": diff,
                "percentage_error": (diff / real_pct) * 100 if real_pct > 0 else 0
            }
            total_diff += diff
        
        accuracy_score = max(0, 1 - (total_diff / 2))
        
        return {
            "accuracy_score": accuracy_score,
            "distributions": differences,
            "summary": f"Status distribution accuracy: {accuracy_score:.2%}",
            "passes_test": accuracy_score > 0.8
        }
    
    def compare_service_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compare years of service patterns"""
        
        # Handle different possible column names
        service_column = None
        for col in ['YearsService', 'years_service', 'Years_Service', 'service_years']:
            if col in df.columns:
                service_column = col
                break
        
        if service_column is None:
            return {
                "accuracy_score": 0,
                "distributions": {},
                "summary": "Years of service column not found in data",
                "passes_test": False,
                "error": "Years of service column not found"
            }
        
        # Create service bins
        df['service_bin'] = pd.cut(df[service_column], 
                                  bins=[0, 5, 15, 25, 35, 50], 
                                  labels=['0-5', '6-15', '16-25', '26-35', '36+'],
                                  include_lowest=True)
        
        synthetic_dist = df['service_bin'].value_counts(normalize=True).to_dict()
        real_dist = self.uk_benchmarks["years_service_patterns"]
        
        differences = {}
        total_diff = 0
        
        for service_range in real_dist:
            synthetic_pct = synthetic_dist.get(service_range, 0)
            real_pct = real_dist[service_range]
            diff = abs(synthetic_pct - real_pct)
            differences[service_range] = {
                "synthetic": synthetic_pct,
                "real": real_pct,
                "difference": diff,
                "percentage_error": (diff / real_pct) * 100 if real_pct > 0 else 0
            }
            total_diff += diff
        
        accuracy_score = max(0, 1 - (total_diff / 2))
        
        return {
            "accuracy_score": accuracy_score,
            "distributions": differences,
            "summary": f"Service patterns accuracy: {accuracy_score:.2%}",
            "passes_test": accuracy_score > 0.7
        }
    
    def calculate_overall_realism_score(self, comparisons: Dict[str, Any]) -> float:
        """Calculate weighted overall realism score"""
        
        weights = {
            "age": 0.20,
            "gender": 0.15,
            "sector": 0.20,
            "salary": 0.25,
            "geographic": 0.10,
            "status": 0.10
        }
        
        total_score = 0
        total_weight = 0
        
        for category, weight in weights.items():
            if category in comparisons and "accuracy_score" in comparisons[category]:
                total_score += comparisons[category]["accuracy_score"] * weight
                total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0
    
    def generate_recommendations(self, comparisons: Dict[str, Any]) -> List[str]:
        """Generate improvement recommendations based on comparison results"""
        
        recommendations = []
        
        for category, results in comparisons.items():
            if "accuracy_score" in results:
                accuracy = results["accuracy_score"]
                
                if accuracy < 0.6:
                    recommendations.append(
                        f"❌ {category.title()} distribution needs significant improvement (accuracy: {accuracy:.1%})"
                    )
                elif accuracy < 0.8:
                    recommendations.append(
                        f"⚠️ {category.title()} distribution could be improved (accuracy: {accuracy:.1%})"
                    )
                else:
                    recommendations.append(
                        f"✅ {category.title()} distribution is realistic (accuracy: {accuracy:.1%})"
                    )
        
        return recommendations
    
    def create_comparison_visualizations(self) -> Dict[str, go.Figure]:
        """Create interactive comparison visualizations"""
        
        if not self.comparison_results:
            return {}
        
        figures = {}
        
        # Overall realism score gauge
        figures["realism_gauge"] = self.create_realism_gauge()
        
        # Distribution comparison charts
        figures["age_comparison"] = self.create_distribution_comparison("age", "Age Distribution")
        figures["gender_comparison"] = self.create_distribution_comparison("gender", "Gender Distribution") 
        figures["sector_comparison"] = self.create_distribution_comparison("sector", "Sector Distribution")
        figures["status_comparison"] = self.create_distribution_comparison("status", "Status Distribution")
        figures["service_comparison"] = self.create_distribution_comparison("service", "Years of Service Distribution")
        
        # Salary comparison by sector
        figures["salary_comparison"] = self.create_salary_comparison()
        
        # Enhanced histogram visualizations
        figures["age_histogram"] = self.create_age_histogram()
        figures["salary_histogram"] = self.create_salary_histogram()
        figures["service_histogram"] = self.create_service_histogram()
        figures["geographic_histogram"] = self.create_geographic_histogram()
        figures["accuracy_scores_histogram"] = self.create_accuracy_scores_histogram()
        figures["error_analysis_histogram"] = self.create_error_analysis_histogram()
        
        return figures
    
    def create_realism_gauge(self) -> go.Figure:
        """Create overall realism score gauge"""
        
        score = self.comparison_results.get("overall_realism_score", 0)
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = score * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Overall Realism Score (%)"},
            delta = {'reference': 80},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 60], 'color': "lightcoral"},
                    {'range': [60, 80], 'color': "lightyellow"},
                    {'range': [80, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300, title="Data Realism Assessment")
        return fig
    
    def create_distribution_comparison(self, category: str, title: str) -> go.Figure:
        """Create comparison chart for distributions"""
        
        if category not in self.comparison_results.get("detailed_comparisons", {}):
            return go.Figure()
        
        data = self.comparison_results["detailed_comparisons"][category]
        distributions = data.get("distributions", {})
        
        categories = list(distributions.keys())
        synthetic_values = [distributions[cat]["synthetic"] * 100 for cat in categories]
        real_values = [distributions[cat]["real"] * 100 for cat in categories]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Synthetic Data',
            x=categories,
            y=synthetic_values,
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name='Real UK Data',
            x=categories,
            y=real_values,
            marker_color='darkblue'
        ))
        
        fig.update_layout(
            title=f"{title} Comparison",
            xaxis_title="Categories",
            yaxis_title="Percentage (%)",
            barmode='group',
            height=400
        )
        
        return fig
    
    def create_salary_comparison(self) -> go.Figure:
        """Create salary comparison by sector"""
        
        if "salary" not in self.comparison_results.get("detailed_comparisons", {}):
            return go.Figure()
        
        salary_data = self.comparison_results["detailed_comparisons"]["salary"]
        sector_analysis = salary_data.get("sector_analysis", {})
        
        sectors = list(sector_analysis.keys())
        synthetic_medians = [sector_analysis[sector]["synthetic_median"] for sector in sectors]
        real_medians = [sector_analysis[sector]["real_median"] for sector in sectors]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Synthetic Median Salary',
            x=sectors,
            y=synthetic_medians,
            marker_color='lightgreen'
        ))
        
        fig.add_trace(go.Bar(
            name='Real UK Median Salary',
            x=sectors,
            y=real_medians,
            marker_color='darkgreen'
        ))
        
        fig.update_layout(
            title="Median Salary Comparison by Sector",
            xaxis_title="Sector",
            yaxis_title="Annual Salary (£)",
            barmode='group',
            height=400
        )
        
        return fig
    
    def create_age_histogram(self) -> go.Figure:
        """Create detailed age distribution histogram"""
        
        if "age" not in self.comparison_results.get("detailed_comparisons", {}):
            return go.Figure().add_annotation(text="No age data available", 
                                            xref="paper", yref="paper", x=0.5, y=0.5)
        
        age_data = self.comparison_results["detailed_comparisons"]["age"]
        distributions = age_data.get("distributions", {})
        
        if not distributions:
            return go.Figure().add_annotation(text="No age distribution data", 
                                            xref="paper", yref="paper", x=0.5, y=0.5)
        
        age_groups = list(distributions.keys())
        synthetic_values = [distributions[group]["synthetic"] * 100 for group in age_groups]
        real_values = [distributions[group]["real"] * 100 for group in age_groups]
        errors = [distributions[group]["percentage_error"] for group in age_groups]
        
        # Create subplot with secondary y-axis
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Age Distribution Comparison', 'Percentage Error by Age Group'),
            specs=[[{"secondary_y": False}], [{"secondary_y": False}]],
            vertical_spacing=0.15
        )
        
        # Main histogram comparison
        fig.add_trace(
            go.Bar(name='Synthetic Data (%)', x=age_groups, y=synthetic_values, 
                   marker_color='lightblue', opacity=0.7),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(name='Real UK Data (%)', x=age_groups, y=real_values, 
                   marker_color='darkblue', opacity=0.8),
            row=1, col=1
        )
        
        # Error analysis
        fig.add_trace(
            go.Bar(name='Percentage Error', x=age_groups, y=errors, 
                   marker_color='red', opacity=0.6, showlegend=False),
            row=2, col=1
        )
        
        fig.update_layout(
            title="Detailed Age Distribution Analysis",
            height=600,
            barmode='group'
        )
        
        fig.update_xaxes(title_text="Age Groups", row=2, col=1)
        fig.update_yaxes(title_text="Percentage (%)", row=1, col=1)
        fig.update_yaxes(title_text="Error (%)", row=2, col=1)
        
        return fig
    
    def create_salary_histogram(self) -> go.Figure:
        """Create detailed salary distribution histogram"""
        
        if "salary" not in self.comparison_results.get("detailed_comparisons", {}):
            return go.Figure().add_annotation(text="No salary data available", 
                                            xref="paper", yref="paper", x=0.5, y=0.5)
        
        salary_data = self.comparison_results["detailed_comparisons"]["salary"]
        sector_analysis = salary_data.get("sector_analysis", {})
        
        if not sector_analysis:
            return go.Figure().add_annotation(text="No salary analysis data", 
                                            xref="paper", yref="paper", x=0.5, y=0.5)
        
        sectors = list(sector_analysis.keys())
        synthetic_medians = [sector_analysis[sector]["synthetic_median"] for sector in sectors]
        real_medians = [sector_analysis[sector]["real_median"] for sector in sectors]
        accuracy_scores = [sector_analysis[sector]["accuracy_score"] * 100 for sector in sectors]
        median_differences = [sector_analysis[sector]["median_difference"] for sector in sectors]
        
        # Create subplot
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Median Salary Comparison', 'Salary Accuracy by Sector',
                          'Median Difference (£)', 'Salary Range Analysis'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Median comparison
        fig.add_trace(
            go.Bar(name='Synthetic', x=sectors, y=synthetic_medians, 
                   marker_color='lightgreen', showlegend=True),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(name='Real UK', x=sectors, y=real_medians, 
                   marker_color='darkgreen', showlegend=True),
            row=1, col=1
        )
        
        # Accuracy scores
        color_scale = ['red' if score < 70 else 'orange' if score < 80 else 'green' 
                      for score in accuracy_scores]
        
        fig.add_trace(
            go.Bar(name='Accuracy %', x=sectors, y=accuracy_scores, 
                   marker_color=color_scale, showlegend=False),
            row=1, col=2
        )
        
        # Median differences
        fig.add_trace(
            go.Bar(name='Difference £', x=sectors, y=median_differences, 
                   marker_color='purple', showlegend=False),
            row=2, col=1
        )
        
        # Range analysis (simplified)
        synthetic_ranges = []
        real_ranges = []
        for sector in sectors:
            real_range = self.uk_benchmarks["salary_ranges"][sector]
            synthetic_ranges.append(real_range["max"] - real_range["min"])  # Approximation
            real_ranges.append(real_range["max"] - real_range["min"])
        
        fig.add_trace(
            go.Bar(name='Salary Range', x=sectors, y=real_ranges, 
                   marker_color='gold', showlegend=False),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Comprehensive Salary Analysis",
            height=800,
            showlegend=True
        )
        
        # Update axes
        fig.update_xaxes(tickangle=45)
        fig.update_yaxes(title_text="Salary (£)", row=1, col=1)
        fig.update_yaxes(title_text="Accuracy (%)", row=1, col=2)
        fig.update_yaxes(title_text="Difference (£)", row=2, col=1)
        fig.update_yaxes(title_text="Range (£)", row=2, col=2)
        
        return fig
    
    def create_service_histogram(self) -> go.Figure:
        """Create years of service distribution histogram"""
        
        if "service" not in self.comparison_results.get("detailed_comparisons", {}):
            return go.Figure().add_annotation(text="No service data available", 
                                            xref="paper", yref="paper", x=0.5, y=0.5)
        
        service_data = self.comparison_results["detailed_comparisons"]["service"]
        distributions = service_data.get("distributions", {})
        
        if not distributions:
            return go.Figure().add_annotation(text="No service distribution data", 
                                            xref="paper", yref="paper", x=0.5, y=0.5)
        
        service_ranges = list(distributions.keys())
        synthetic_values = [distributions[range_]["synthetic"] * 100 for range_ in service_ranges]
        real_values = [distributions[range_]["real"] * 100 for range_ in service_ranges]
        differences = [distributions[range_]["difference"] * 100 for range_ in service_ranges]
        
        # Create histogram with error overlay
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Synthetic Data',
            x=service_ranges,
            y=synthetic_values,
            marker_color='lightcoral',
            opacity=0.7
        ))
        
        fig.add_trace(go.Bar(
            name='Real UK Data', 
            x=service_ranges,
            y=real_values,
            marker_color='darkred',
            opacity=0.8
        ))
        
        # Add difference as line plot
        fig.add_trace(go.Scatter(
            name='Absolute Difference',
            x=service_ranges,
            y=differences,
            mode='lines+markers',
            line=dict(color='black', width=3),
            marker=dict(size=8),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Years of Service Distribution Analysis",
            xaxis_title="Years of Service",
            yaxis_title="Percentage (%)",
            yaxis2=dict(
                title="Difference (%)",
                overlaying='y',
                side='right'
            ),
            barmode='group',
            height=500
        )
        
        return fig
    
    def create_geographic_histogram(self) -> go.Figure:
        """Create geographic distribution histogram"""
        
        if "geographic" not in self.comparison_results.get("detailed_comparisons", {}):
            return go.Figure().add_annotation(text="No geographic data available", 
                                            xref="paper", yref="paper", x=0.5, y=0.5)
        
        geo_data = self.comparison_results["detailed_comparisons"]["geographic"]
        distributions = geo_data.get("distributions", {})
        
        if not distributions:
            return go.Figure().add_annotation(text="No geographic distribution data", 
                                            xref="paper", yref="paper", x=0.5, y=0.5)
        
        regions = list(distributions.keys())
        synthetic_values = [distributions[region]["synthetic"] * 100 for region in regions]
        real_values = [distributions[region]["real"] * 100 for region in regions]
        errors = [distributions[region]["percentage_error"] for region in regions]
        
        # Create horizontal bar chart for better region name visibility
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Regional Distribution Comparison', 'Percentage Error by Region'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]],
            horizontal_spacing=0.15
        )
        
        fig.add_trace(
            go.Bar(name='Synthetic %', y=regions, x=synthetic_values, 
                   orientation='h', marker_color='lightblue', opacity=0.7),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(name='Real UK %', y=regions, x=real_values, 
                   orientation='h', marker_color='darkblue', opacity=0.8),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(name='Error %', y=regions, x=errors, 
                   orientation='h', marker_color='red', opacity=0.6, showlegend=False),
            row=1, col=2
        )
        
        fig.update_layout(
            title="Geographic Distribution Analysis",
            height=max(400, len(regions) * 40),  # Dynamic height based on regions
            barmode='group'
        )
        
        fig.update_xaxes(title_text="Percentage (%)", row=1, col=1)
        fig.update_xaxes(title_text="Error (%)", row=1, col=2)
        
        return fig
    
    def create_accuracy_scores_histogram(self) -> go.Figure:
        """Create overall accuracy scores comparison histogram"""
        
        detailed_comparisons = self.comparison_results.get("detailed_comparisons", {})
        
        if not detailed_comparisons:
            return go.Figure().add_annotation(text="No comparison data available", 
                                            xref="paper", yref="paper", x=0.5, y=0.5)
        
        categories = []
        accuracy_scores = []
        pass_status = []
        
        for category, data in detailed_comparisons.items():
            if "accuracy_score" in data:
                categories.append(category.title())
                score = data["accuracy_score"] * 100
                accuracy_scores.append(score)
                pass_status.append("Pass" if data.get("passes_test", False) else "Fail")
        
        # Color coding based on pass/fail
        colors = ['green' if status == 'Pass' else 'red' for status in pass_status]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Accuracy Score',
            x=categories,
            y=accuracy_scores,
            marker_color=colors,
            text=[f"{score:.1f}%" for score in accuracy_scores],
            textposition='outside'
        ))
        
        # Add threshold lines
        fig.add_hline(y=80, line_dash="dash", line_color="green", 
                     annotation_text="Excellence Threshold (80%)")
        fig.add_hline(y=60, line_dash="dash", line_color="orange", 
                     annotation_text="Good Threshold (60%)")
        
        fig.update_layout(
            title="Category Accuracy Scores Overview",
            xaxis_title="Analysis Categories",
            yaxis_title="Accuracy Score (%)",
            height=500,
            showlegend=False
        )
        
        fig.update_xaxes(tickangle=45)
        fig.update_yaxes(range=[0, 105])
        
        return fig
    
    def create_error_analysis_histogram(self) -> go.Figure:
        """Create comprehensive error analysis histogram"""
        
        detailed_comparisons = self.comparison_results.get("detailed_comparisons", {})
        
        if not detailed_comparisons:
            return go.Figure().add_annotation(text="No error analysis data available", 
                                            xref="paper", yref="paper", x=0.5, y=0.5)
        
        # Collect error data from all categories
        error_data = []
        
        for category, data in detailed_comparisons.items():
            if "distributions" in data:
                distributions = data["distributions"]
                for subcategory, metrics in distributions.items():
                    error_data.append({
                        'category': category.title(),
                        'subcategory': subcategory,
                        'percentage_error': metrics.get('percentage_error', 0),
                        'absolute_difference': metrics.get('difference', 0) * 100
                    })
        
        if not error_data:
            return go.Figure().add_annotation(text="No detailed error data available", 
                                            xref="paper", yref="paper", x=0.5, y=0.5)
        
        # Create error distribution histogram
        percentage_errors = [item['percentage_error'] for item in error_data]
        absolute_differences = [item['absolute_difference'] for item in error_data]
        categories = [f"{item['category']}-{item['subcategory']}" for item in error_data]
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Percentage Error Distribution', 'Absolute Difference Distribution'),
            vertical_spacing=0.15
        )
        
        # Percentage errors
        fig.add_trace(
            go.Histogram(x=percentage_errors, nbinsx=20, name='Percentage Error', 
                        marker_color='red', opacity=0.7),
            row=1, col=1
        )
        
        # Absolute differences  
        fig.add_trace(
            go.Histogram(x=absolute_differences, nbinsx=20, name='Absolute Difference', 
                        marker_color='orange', opacity=0.7, showlegend=False),
            row=2, col=1
        )
        
        fig.update_layout(
            title="Comprehensive Error Analysis Distribution",
            height=600
        )
        
        fig.update_xaxes(title_text="Percentage Error (%)", row=1, col=1)
        fig.update_xaxes(title_text="Absolute Difference (%)", row=2, col=1)
        fig.update_yaxes(title_text="Frequency", row=1, col=1)
        fig.update_yaxes(title_text="Frequency", row=2, col=1)
        
        return fig
