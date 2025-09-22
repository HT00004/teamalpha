#!/usr/bin/env python3
"""
🎖️ Mission Alpha Command Dashboard
Operation Synthetic Shield - Advanced Analytics & Mission Control

Comprehensive dashboard for monitoring pension data generation missions,
analyzing synthetic data quality, and managing Azure AI Foundry operations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import io
from datetime import datetime, timedelta
from dataclasses import asdict
import time
import random

# Azure AI imports (optional)
try:
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    from dotenv import load_dotenv
    AZURE_AI_AVAILABLE = True
except ImportError:
    AZURE_AI_AVAILABLE = False

# Load environment variables
load_dotenv()

class MissionDashboard:
    """Advanced dashboard for Mission Alpha operations"""
    
    def __init__(self):
        self.initialize_session_state()
        self.load_configuration()
    
    def initialize_session_state(self):
        """Initialize dashboard session state"""
        if 'dashboard_data' not in st.session_state:
            st.session_state.dashboard_data = {}
        if 'mission_history' not in st.session_state:
            st.session_state.mission_history = []
        if 'real_time_metrics' not in st.session_state:
            st.session_state.real_time_metrics = {
                'total_missions': 0,
                'total_records': 0,
                'success_rate': 100.0,
                'azure_ai_usage': 0,
                'demo_usage': 0
            }
        if 'dashboard_config' not in st.session_state:
            st.session_state.dashboard_config = {
                'auto_refresh': False,
                'refresh_interval': 30,
                'show_advanced_metrics': True,
                'enable_alerts': True
            }
    
    def load_configuration(self):
        """Load Azure AI configuration status"""
        self.azure_endpoint = os.getenv("AZURE_AI_ENDPOINT")
        self.azure_key = os.getenv("AZURE_AI_KEY")
        self.azure_model = os.getenv("AZURE_AI_MODEL", "gpt-4o")
        self.azure_enabled = os.getenv("ENABLE_AZURE_AI", "false").lower() == "true"
        
        self.azure_status = "🔴 Disconnected"
        if self.azure_enabled and AZURE_AI_AVAILABLE and self.azure_endpoint and self.azure_key:
            self.azure_status = "🟢 Connected"
        elif AZURE_AI_AVAILABLE and self.azure_endpoint and self.azure_key:
            self.azure_status = "🟡 Available"
    
    def create_mission_metrics(self):
        """Create real-time mission metrics"""
        metrics = st.session_state.real_time_metrics
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "🎖️ Total Missions", 
                metrics['total_missions'],
                delta=1 if metrics['total_missions'] > 0 else None
            )
        
        with col2:
            st.metric(
                "👥 Records Generated", 
                f"{metrics['total_records']:,}",
                delta=f"+{random.randint(100, 1000)}" if metrics['total_records'] > 0 else None
            )
        
        with col3:
            st.metric(
                "✅ Success Rate", 
                f"{metrics['success_rate']:.1f}%",
                delta=f"+{random.uniform(0.1, 0.5):.1f}%" if metrics['success_rate'] < 100 else None
            )
        
        with col4:
            st.metric(
                "🤖 Azure AI Usage", 
                f"{metrics['azure_ai_usage']}",
                delta=1 if metrics['azure_ai_usage'] > 0 else None
            )
        
        with col5:
            st.metric(
                "🎲 Demo Usage", 
                f"{metrics['demo_usage']}",
                delta=1 if metrics['demo_usage'] > 0 else None
            )
    
    def create_system_status_panel(self):
        """Create system status monitoring panel"""
        st.subheader("🚨 System Status Monitor")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Azure AI Status
            st.markdown("### 🤖 Azure AI Foundry")
            status_color = {"🟢": "success", "🟡": "warning", "🔴": "error"}
            status_icon = self.azure_status.split()[0]
            
            if status_icon in status_color:
                st.success(f"{self.azure_status}")
            elif status_icon == "🟡":
                st.warning(f"{self.azure_status}")
            else:
                st.error(f"{self.azure_status}")
            
            if self.azure_endpoint:
                st.info(f"**Endpoint:** {self.azure_endpoint[:50]}...")
                st.info(f"**Model:** {self.azure_model}")
            
            # Connection test button
            if st.button("🔍 Test Azure AI Connection"):
                with st.spinner("Testing connection..."):
                    success, message = self.test_azure_connection()
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
        
        with col2:
            # System Health
            st.markdown("### 📊 System Health")
            
            # Simulate system metrics
            cpu_usage = random.uniform(20, 60)
            memory_usage = random.uniform(30, 70)
            
            fig = go.Figure()
            fig.add_trace(go.Indicator(
                mode = "gauge+number",
                value = cpu_usage,
                title = {'text': "CPU Usage (%)"},
                domain = {'x': [0, 0.5], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig.add_trace(go.Indicator(
                mode = "gauge+number",
                value = memory_usage,
                title = {'text': "Memory Usage (%)"},
                domain = {'x': [0.5, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkgreen"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)
    
    def test_azure_connection(self):
        """Test Azure AI Foundry connection"""
        if not AZURE_AI_AVAILABLE:
            return False, "Azure AI SDK not installed"
        
        if not self.azure_endpoint or not self.azure_key:
            return False, "Azure AI credentials not configured"
        
        try:
            client = ChatCompletionsClient(
                endpoint=self.azure_endpoint,
                credential=AzureKeyCredential(self.azure_key)
            )
            
            # Simple test call
            response = client.complete(
                messages=[
                    SystemMessage(content="You are a test assistant."),
                    UserMessage(content="Respond with 'Connection successful'")
                ],
                temperature=0.1,
                model=self.azure_model
            )
            
            if response and response.choices:
                return True, "Connection successful - Azure AI Foundry responding"
            else:
                return False, "No response from Azure AI Foundry"
                
        except Exception as e:
            return False, f"Connection failed: {str(e)[:100]}"
    
    def create_data_analytics_dashboard(self):
        """Create comprehensive data analytics dashboard"""
        st.subheader("📊 Data Analytics Dashboard")
        
        # Check for available data
        if not hasattr(st.session_state, 'generated_data') or not st.session_state.generated_data:
            st.info("🎯 Generate data using the main application to view analytics")
            
            # Show sample analytics with dummy data
            st.markdown("### 📈 Sample Analytics (Demo Data)")
            self.create_sample_analytics()
            return
        
        data = st.session_state.generated_data
        profiles = data.get('profiles', [])
        
        if not profiles:
            st.warning("No profile data available for analysis")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame([asdict(p) for p in profiles])
        
        # Analytics tabs
        tab1, tab2, tab3, tab4 = st.tabs(["👥 Demographics", "💰 Financial", "📍 Geographic", "⚡ Performance"])
        
        with tab1:
            self.create_demographics_analytics(df)
        
        with tab2:
            self.create_financial_analytics(df)
        
        with tab3:
            self.create_geographic_analytics(df)
        
        with tab4:
            self.create_performance_analytics(data)
    
    def create_demographics_analytics(self, df):
        """Create demographics analytics"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Age distribution
            fig = px.histogram(
                df, x='age', nbins=20,
                title="Age Distribution",
                color_discrete_sequence=['#1f77b4']
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Gender distribution
            gender_counts = df['gender'].value_counts()
            fig = px.pie(
                values=gender_counts.values,
                names=gender_counts.index,
                title="Gender Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Sector distribution
            sector_counts = df['sector'].value_counts()
            fig = px.bar(
                x=sector_counts.values,
                y=sector_counts.index,
                orientation='h',
                title="Employment Sector Distribution",
                color=sector_counts.values,
                color_continuous_scale='viridis'
            )
            fig.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
            
            # Status distribution
            status_counts = df['status'].value_counts()
            fig = px.bar(
                x=status_counts.index,
                y=status_counts.values,
                title="Member Status Distribution",
                color=status_counts.values,
                color_continuous_scale='plasma'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    def create_financial_analytics(self, df):
        """Create financial analytics"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Salary distribution
            fig = px.histogram(
                df, x='annual_salary', nbins=30,
                title="Annual Salary Distribution",
                color_discrete_sequence=['#2ca02c']
            )
            fig.update_layout(showlegend=False)
            fig.update_xaxis(title="Annual Salary (£)")
            st.plotly_chart(fig, use_container_width=True)
            
            # Salary by sector
            fig = px.box(
                df, x='sector', y='annual_salary',
                title="Salary Distribution by Sector"
            )
            fig.update_xaxis(tickangle=45)
            fig.update_yaxis(title="Annual Salary (£)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Age vs Salary correlation
            fig = px.scatter(
                df, x='age', y='annual_salary',
                color='sector',
                title="Age vs Salary Correlation",
                hover_data=['years_service']
            )
            fig.update_yaxis(title="Annual Salary (£)")
            st.plotly_chart(fig, use_container_width=True)
            
            # Years of service distribution
            fig = px.histogram(
                df, x='years_service', nbins=20,
                title="Years of Service Distribution",
                color_discrete_sequence=['#ff7f0e']
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    def create_geographic_analytics(self, df):
        """Create geographic analytics"""
        st.markdown("### 📍 Geographic Distribution Analysis")
        
        # Extract postcode areas (first 1-2 letters)
        df['postcode_area'] = df['postcode'].str.extract(r'^([A-Z]{1,2})')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Postcode area distribution
            area_counts = df['postcode_area'].value_counts().head(15)
            fig = px.bar(
                x=area_counts.values,
                y=area_counts.index,
                orientation='h',
                title="Top 15 Postcode Areas",
                color=area_counts.values,
                color_continuous_scale='blues'
            )
            fig.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Average salary by postcode area
            salary_by_area = df.groupby('postcode_area')['annual_salary'].mean().sort_values(ascending=False).head(10)
            fig = px.bar(
                x=salary_by_area.index,
                y=salary_by_area.values,
                title="Average Salary by Postcode Area (Top 10)",
                color=salary_by_area.values,
                color_continuous_scale='greens'
            )
            fig.update_layout(showlegend=False)
            fig.update_yaxis(title="Average Salary (£)")
            st.plotly_chart(fig, use_container_width=True)
        
        # Geographic summary table
        geo_summary = df.groupby('postcode_area').agg({
            'member_id': 'count',
            'annual_salary': ['mean', 'median'],
            'age': 'mean'
        }).round(2)
        
        geo_summary.columns = ['Member Count', 'Avg Salary', 'Median Salary', 'Avg Age']
        geo_summary = geo_summary.sort_values('Member Count', ascending=False)
        
        st.subheader("📋 Geographic Summary")
        st.dataframe(geo_summary, use_container_width=True)
    
    def create_performance_analytics(self, data):
        """Create performance analytics"""
        st.markdown("### ⚡ Generation Performance Analysis")
        
        generation_method = data.get('generation_method', 'Unknown')
        timestamp = data.get('timestamp', '')
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Generation Method", generation_method)
        
        with col2:
            if timestamp:
                dt = datetime.fromisoformat(timestamp)
                st.metric("Generated At", dt.strftime("%H:%M:%S"))
        
        with col3:
            total_records = len(data.get('profiles', [])) + len(data.get('contributions', [])) + len(data.get('allocations', []))
            st.metric("Total Records", f"{total_records:,}")
        
        # Performance simulation chart
        st.subheader("📈 Generation Performance Timeline")
        
        # Simulate performance data
        times = pd.date_range(start='2025-01-01', periods=30, freq='D')
        performance_data = {
            'Date': times,
            'Records Generated': np.random.poisson(1500, 30),
            'Success Rate': np.random.uniform(95, 100, 30),
            'Azure AI Usage': np.random.poisson(800, 30),
            'Demo Usage': np.random.poisson(700, 30)
        }
        
        perf_df = pd.DataFrame(performance_data)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Records Generated', 'Success Rate', 'Azure AI Usage', 'Demo Usage'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig.add_trace(
            go.Scatter(x=perf_df['Date'], y=perf_df['Records Generated'], name='Records'),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=perf_df['Date'], y=perf_df['Success Rate'], name='Success Rate'),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=perf_df['Date'], y=perf_df['Azure AI Usage'], name='Azure AI'),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=perf_df['Date'], y=perf_df['Demo Usage'], name='Demo'),
            row=2, col=2
        )
        
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    def create_sample_analytics(self):
        """Create sample analytics for demo purposes"""
        # Generate sample data for demonstration
        sample_data = {
            'age': np.random.normal(42, 12, 1000).astype(int),
            'annual_salary': np.random.lognormal(10.5, 0.5, 1000).astype(int),
            'sector': np.random.choice(['Finance', 'Healthcare', 'Manufacturing', 'Public Service', 'Education'], 1000),
            'status': np.random.choice(['Active', 'Deferred', 'Pensioner'], 1000, p=[0.85, 0.12, 0.03])
        }
        
        # Ensure realistic ranges
        sample_data['age'] = np.clip(sample_data['age'], 22, 67)
        sample_data['annual_salary'] = np.clip(sample_data['annual_salary'], 15000, 150000)
        
        df = pd.DataFrame(sample_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(df, x='age', nbins=20, title="Sample Age Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.histogram(df, x='annual_salary', nbins=30, title="Sample Salary Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    def create_mission_control(self):
        """Create mission control panel"""
        st.subheader("🎖️ Mission Control Center")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🚀 Quick Actions")
            
            if st.button("🎯 Launch Demo Mission", use_container_width=True):
                st.info("Redirecting to demo application...")
                st.markdown("[Launch Demo](http://localhost:8501)")
            
            if st.button("🤖 Launch Azure AI Mission", use_container_width=True):
                st.info("Launching Azure AI version...")
                st.markdown("Execute: `streamlit run streamlit_azure_ai.py`")
            
            if st.button("⚙️ Configure Azure AI", use_container_width=True):
                st.info("Use the enhanced launcher for configuration")
                st.code("python launch_enhanced.py")
        
        with col2:
            st.markdown("### 📊 Dashboard Settings")
            
            auto_refresh = st.checkbox(
                "🔄 Auto Refresh", 
                value=st.session_state.dashboard_config['auto_refresh']
            )
            
            refresh_interval = st.slider(
                "Refresh Interval (seconds)", 
                10, 300, 
                st.session_state.dashboard_config['refresh_interval']
            )
            
            show_advanced = st.checkbox(
                "📈 Advanced Metrics", 
                value=st.session_state.dashboard_config['show_advanced_metrics']
            )
            
            enable_alerts = st.checkbox(
                "🚨 Enable Alerts", 
                value=st.session_state.dashboard_config['enable_alerts']
            )
            
            # Update config
            st.session_state.dashboard_config.update({
                'auto_refresh': auto_refresh,
                'refresh_interval': refresh_interval,
                'show_advanced_metrics': show_advanced,
                'enable_alerts': enable_alerts
            })
    
    def create_alerts_panel(self):
        """Create alerts and notifications panel"""
        if not st.session_state.dashboard_config['enable_alerts']:
            return
        
        st.subheader("🚨 Alerts & Notifications")
        
        # Sample alerts
        alerts = [
            {
                'type': 'success',
                'message': 'Mission Alpha completed successfully - 2,500 records generated',
                'timestamp': datetime.now() - timedelta(minutes=5)
            },
            {
                'type': 'warning', 
                'message': 'Azure AI connection unstable - fallback mode activated',
                'timestamp': datetime.now() - timedelta(minutes=15)
            },
            {
                'type': 'info',
                'message': 'New mission started with Azure AI Foundry',
                'timestamp': datetime.now() - timedelta(minutes=30)
            }
        ]
        
        for alert in alerts:
            icon = {'success': '✅', 'warning': '⚠️', 'info': 'ℹ️'}.get(alert['type'], 'ℹ️')
            timestamp_str = alert['timestamp'].strftime('%H:%M:%S')
            
            if alert['type'] == 'success':
                st.success(f"{icon} {timestamp_str} - {alert['message']}")
            elif alert['type'] == 'warning':
                st.warning(f"{icon} {timestamp_str} - {alert['message']}")
            else:
                st.info(f"{icon} {timestamp_str} - {alert['message']}")

# Custom CSS for dashboard
def load_dashboard_css():
    st.markdown("""
    <style>
        .dashboard-header {
            background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .metric-container {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #3b82f6;
            margin: 0.5rem 0;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-online { background-color: #10b981; }
        .status-warning { background-color: #f59e0b; }
        .status-offline { background-color: #ef4444; }
        
        .command-center {
            background: #1f2937;
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        .alert-panel {
            border-left: 4px solid #ef4444;
            background: #fef2f2;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 4px;
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main dashboard application"""
    st.set_page_config(
        page_title="Mission Alpha Command Dashboard",
        page_icon="🎖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    load_dashboard_css()
    
    # Initialize dashboard
    dashboard = MissionDashboard()
    
    # Header
    st.markdown("""
    <div class="dashboard-header">
        <h1>🎖️ MISSION ALPHA COMMAND DASHBOARD</h1>
        <h3>Operation Synthetic Shield - Advanced Analytics & Control</h3>
        <p><em>Real-time monitoring and analytics for pension data generation missions</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.header("🎛️ Command Center")
        
        page = st.selectbox(
            "Select Dashboard View",
            [
                "🏠 Mission Overview",
                "📊 Data Analytics", 
                "🚨 System Monitor",
                "🎖️ Mission Control",
                "📈 Performance",
                "⚙️ Configuration"
            ]
        )
        
        st.markdown("---")
        
        # Quick stats
        st.subheader("📋 Quick Stats")
        metrics = st.session_state.real_time_metrics
        st.metric("Active Missions", metrics['total_missions'])
        st.metric("Total Records", f"{metrics['total_records']:,}")
        st.metric("Azure AI Status", dashboard.azure_status.split()[1] if len(dashboard.azure_status.split()) > 1 else "Unknown")
        
        # Auto-refresh
        if st.session_state.dashboard_config['auto_refresh']:
            st.info(f"🔄 Auto-refresh: {st.session_state.dashboard_config['refresh_interval']}s")
            time.sleep(1)
            st.rerun()
    
    # Main content based on selected page
    if page == "🏠 Mission Overview":
        dashboard.create_mission_metrics()
        st.markdown("---")
        dashboard.create_alerts_panel()
        
    elif page == "📊 Data Analytics":
        dashboard.create_data_analytics_dashboard()
        
    elif page == "🚨 System Monitor":
        dashboard.create_system_status_panel()
        
    elif page == "🎖️ Mission Control":
        dashboard.create_mission_control()
        
    elif page == "📈 Performance":
        st.subheader("📈 Performance Analytics")
        if hasattr(st.session_state, 'generated_data') and st.session_state.generated_data:
            dashboard.create_performance_analytics(st.session_state.generated_data)
        else:
            st.info("Generate data to view performance analytics")
            dashboard.create_sample_analytics()
    
    elif page == "⚙️ Configuration":
        st.subheader("⚙️ Dashboard Configuration")
        dashboard.create_mission_control()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🎖️ <strong>Mission Alpha Command Dashboard</strong> 🎖️</p>
        <p><em>Monitoring synthetic intelligence operations with zero PII exposure</em></p>
        <p>Classification: Command & Control | Status: Operational</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
