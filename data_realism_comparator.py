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
            # Load synthetic data
            synthetic_df = pd.read_csv(synthetic_data_path)
            
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
        
        # Create age bins
        df['age_bin'] = pd.cut(df['Age'], 
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
        
        synthetic_dist = df['Gender'].value_counts(normalize=True).to_dict()
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
        
        synthetic_dist = df['Sector'].value_counts(normalize=True).to_dict()
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
        
        sector_salary_analysis = {}
        overall_accuracy = 0
        
        for sector in self.uk_benchmarks["salary_ranges"]:
            sector_data = df[df['Sector'] == sector]['AnnualSalary']
            
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
        df['postcode_area'] = df['Postcode'].str.split(' ').str[0]
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
        
        synthetic_dist = df['Status'].value_counts(normalize=True).to_dict()
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
        
        # Create service bins
        df['service_bin'] = pd.cut(df['YearsService'], 
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
        
        # Salary comparison by sector
        figures["salary_comparison"] = self.create_salary_comparison()
        
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
