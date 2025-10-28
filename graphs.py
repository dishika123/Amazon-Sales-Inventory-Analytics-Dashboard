import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
def load_data():
    # Load international sales data
    international_data = pd.read_csv("new_international_sales_report.csv")
    # Load stock report
    stock_report = pd.read_csv("new_stock_report.csv")
    
    # Merge datasets on SKU with left join
    df = pd.merge(
        international_data,
        stock_report,
        on='sku',
        how='left',
        suffixes=('', '_report')
    )
    
    # Convert date string to datetime with specific format (DD-MM-YYYY)
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    # Extract year and month
    df['Year'] = df['date'].dt.year
    df['Month'] = df['date'].dt.strftime('%B')
    return df

def main():
    st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")
    
    # Custom CSS for attractive tabs
    st.markdown("""
        <style>
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background-color: #1e1e1e;
            padding: 10px;
            border-radius: 10px;
            display: flex;
            justify-content: space-between;
        }
        
        .stTabs [data-baseweb="tab"] {
            flex: 1;
            height: 70px;
            background-color: #2d2d2d;
            border-radius: 8px;
            padding: 15px 10px;
            font-size: 18px;
            font-weight: 700;
            color: #ffffff;
            border: 2px solid transparent;
            transition: all 0.3s ease;
            white-space: normal;
            text-align: center;
            line-height: 1.3;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
            border-color: #f5576c !important;
            box-shadow: 0 4px 20px rgba(245, 87, 108, 0.5) !important;
            transform: scale(1.05);
        }
        
        /* Dashboard title styling */
        h1 {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3em !important;
            font-weight: 800 !important;
            text-align: center;
            padding: 20px 0;
            text-shadow: 0 0 30px rgba(245, 87, 108, 0.5);
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from {
                text-shadow: 0 0 20px rgba(245, 87, 108, 0.5), 0 0 30px rgba(240, 147, 251, 0.3);
            }
            to {
                text-shadow: 0 0 30px rgba(245, 87, 108, 0.8), 0 0 40px rgba(240, 147, 251, 0.5);
            }
        }
        
        /* Metric cards styling */
        [data-testid="stMetricValue"] {
            font-size: 28px;
            font-weight: 700;
            color: #667eea;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 14px;
            font-weight: 600;
            color: #a0a0a0;
        }
        
        /* Add animation to metrics */
        div[data-testid="metric-container"] {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(102, 126, 234, 0.2);
            transition: all 0.3s ease;
        }
        
        div[data-testid="metric-container"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
            border-color: rgba(102, 126, 234, 0.5);
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("Amazon Sales & Inventory Analytics Dashboard")
    
    # Load data
    df = load_data()
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Sales Overview", 
        "🔍 Product Analysis", 
        "📦 Inventory Stock", 
        "↩️ Product Returns", 
        "🔗 Stock & Returns Correlation", 
        "👥 Customer Insights", 
        "💰 Profit Margin Analysis"
    ])
    
    with tab1:
        # Year filter (common for all visualizations)
        # Use years that exist in international sales data
        years = sorted(df['Year'].unique())
        selected_year = st.selectbox("Select Year", years)
        
        # Filter data based on selected year
        filtered_df = df[df['Year'] == selected_year]
        
        # ==================== KPI METRICS ====================
        st.markdown("---")
        st.subheader(f"📊 Key Performance Indicators - {selected_year}")
        
        # Calculate KPIs
        total_sales = filtered_df['Gross_Amount'].sum()
        total_quantity = filtered_df['Quantity_Purchased'].sum()
        total_orders = len(filtered_df)
        avg_order_value = total_sales / total_orders if total_orders > 0 else 0
        
        # Display KPIs in columns
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        with kpi_col1:
            st.metric(
                label="💰 Total Sales",
                value=f"₹{total_sales:,.0f}",
                help="Total gross sales amount for the selected year"
            )
        
        with kpi_col2:
            st.metric(
                label="📦 Total Quantity Sold",
                value=f"{total_quantity:,.0f}",
                help="Total quantity of products sold"
            )
        
        with kpi_col3:
            st.metric(
                label="🛒 Total Orders",
                value=f"{total_orders:,}",
                help="Total number of orders placed"
            )
        
        with kpi_col4:
            st.metric(
                label="💵 Avg Order Value",
                value=f"₹{avg_order_value:,.0f}",
                help="Average value per order"
            )
        
        # Additional KPIs row
        st.markdown("")  # Add spacing
        kpi_col5, kpi_col6, kpi_col7, kpi_col8 = st.columns(4)
        
        with kpi_col5:
            unique_categories = filtered_df['category'].nunique() if 'category' in filtered_df.columns else 0
            st.metric(
                label="🏷️ Product Categories",
                value=f"{unique_categories}",
                help="Number of unique product categories"
            )
        
        with kpi_col6:
            unique_products = filtered_df['SKU Code'].nunique() if 'SKU Code' in filtered_df.columns else 0
            st.metric(
                label="🔖 Unique Products",
                value=f"{unique_products:,}",
                help="Number of unique SKU codes sold"
            )
        
        with kpi_col7:
            # Calculate best selling month
            monthly_totals = filtered_df.groupby('Month')['Gross_Amount'].sum()
            best_month = monthly_totals.idxmax() if len(monthly_totals) > 0 else "N/A"
            best_month_sales = monthly_totals.max() if len(monthly_totals) > 0 else 0
            st.metric(
                label="📅 Best Month",
                value=best_month,
                delta=f"₹{best_month_sales:,.0f}",
                help="Month with highest sales"
            )
        
        with kpi_col8:
            # Calculate average monthly sales
            avg_monthly_sales = filtered_df.groupby('Month')['Gross_Amount'].sum().mean()
            st.metric(
                label="📈 Avg Monthly Sales",
                value=f"₹{avg_monthly_sales:,.0f}",
                help="Average sales per month"
            )
        
        st.markdown("---")
        
        # Create monthly summary
        monthly_sales = filtered_df.groupby('Month')['Gross_Amount'].sum().reset_index()
        
        # Sort months chronologically
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December']
        monthly_sales['Month'] = pd.Categorical(monthly_sales['Month'], categories=month_order, ordered=True)
        monthly_sales = monthly_sales.sort_values('Month')
        
        # Add numeric index for trend line
        monthly_sales['Month_Num'] = range(len(monthly_sales))
        
        # Create bar chart using plotly
        fig = px.bar(monthly_sales, 
                     x='Month', 
                     y='Gross_Amount',
                     title=f'Monthly Gross Sales for {selected_year}',
                     labels={'Gross_Amount': 'Gross Amount (₹)'})
        
        # Add trend line
        import plotly.graph_objects as go
        from scipy import stats
        
        # Calculate linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(monthly_sales['Month_Num'], monthly_sales['Gross_Amount'])
        trend_line = slope * monthly_sales['Month_Num'] + intercept
        
        # Add trend line to the chart
        fig.add_trace(go.Scatter(
            x=monthly_sales['Month'],
            y=trend_line,
            mode='lines',
            name='Trend',
            line=dict(color='red', width=3, dash='dash')
        ))
        
        # Update layout
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Gross Amount (₹)",
            bargap=0.2,
            height=600,
            showlegend=True
        )
        
        # Display the plot
        st.plotly_chart(fig, use_container_width=True)
        
        # Add separator
        st.markdown("---")
        st.header("Category-wise Monthly Analysis")
        
        # Check if category data is available
        if 'category' not in filtered_df.columns or filtered_df['category'].isnull().all():
            st.warning(f"No category data available for {selected_year}")
        else:
            # Month order
            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                           'July', 'August', 'September', 'October', 'November', 'December']
            
            # Create pivot table for Sales Heatmap (using Gross_Amount)
            sales_pivot = filtered_df.groupby(['category', 'Month'])['Gross_Amount'].sum().reset_index()
            sales_pivot_table = sales_pivot.pivot(index='category', columns='Month', values='Gross_Amount').fillna(0)
            # Reorder columns by month
            available_months = [m for m in month_order if m in sales_pivot_table.columns]
            sales_pivot_table = sales_pivot_table[available_months]
            
            # Create Sales Heatmap
            fig_sales = px.imshow(sales_pivot_table,
                                  labels=dict(x="Month", y="Category", color="Sales (₹)"),
                                  x=available_months,
                                  y=sales_pivot_table.index,
                                  title=f'Sales Heatmap by Category and Month ({selected_year})',
                                  color_continuous_scale='YlOrRd',
                                  aspect='auto')
            
            fig_sales.update_xaxes(side="bottom")
            fig_sales.update_layout(height=600)
            
            st.plotly_chart(fig_sales, use_container_width=True)
            
            # Create pivot table for Quantity Heatmap (using Quantity_Purchased)
            quantity_pivot = filtered_df.groupby(['category', 'Month'])['Quantity_Purchased'].sum().reset_index()
            quantity_pivot_table = quantity_pivot.pivot(index='category', columns='Month', values='Quantity_Purchased').fillna(0)
            # Reorder columns by month
            quantity_pivot_table = quantity_pivot_table[available_months]
            
            # Create Quantity Heatmap
            fig_quantity = px.imshow(quantity_pivot_table,
                                     labels=dict(x="Month", y="Category", color="Quantity"),
                                     x=available_months,
                                     y=quantity_pivot_table.index,
                                     title=f'Quantity Heatmap by Category and Month ({selected_year})',
                                     color_continuous_scale='Blues',
                                     aspect='auto')
            
            fig_quantity.update_xaxes(side="bottom")
            fig_quantity.update_layout(height=600)
            
            st.plotly_chart(fig_quantity, use_container_width=True)
        
        # Add separator
        st.markdown("---")
        st.header("Top 10 Colors by Sales")
        
        # Check if colour data is available
        if 'colour' not in filtered_df.columns or filtered_df['colour'].isnull().all():
            st.warning(f"No colour data available for {selected_year}")
        else:
            # Group by colour and sum gross amount
            color_sales = filtered_df.groupby('colour')['Gross_Amount'].sum().reset_index()
            # Sort by gross amount and get top 10
            color_sales = color_sales.sort_values('Gross_Amount', ascending=False).head(10)
            
            # Create a color mapping dictionary for common color names
            color_map = {
                'red': 'red',
                'blue': 'blue',
                'green': 'green',
                'yellow': 'yellow',
                'orange': 'orange',
                'pink': 'pink',
                'purple': 'purple',
                'black': 'black',
                'white': 'white',
                'grey': '#808080',
                'gray': '#808080',
                'brown': 'brown',
                'maroon': 'maroon',
                'navy': 'navy',
                'beige': '#F5F5DC',
                'cream': '#FFFDD0',
                'gold': 'gold',
                'silver': 'silver',
                'turquoise': 'turquoise',
                'lavender': 'lavender',
                'peach': 'peachpuff',
                'mint': '#98FF98',
                'coral': 'coral',
                'teal': 'teal',
                'cyan': 'cyan',
                'magenta': 'magenta',
                'olive': 'olive',
                'indigo': 'indigo',
                'violet': 'violet',
                'burgundy': 'darkred',
                'khaki': 'khaki',
                'off white': '#FAF9F6',
                'offwhite': '#FAF9F6',
                'mustard': '#FFDB58',
                'mustard yellow': '#FFDB58'
            }
            
            # Map colors with case-insensitive matching
            color_sales['bar_color'] = color_sales['colour'].apply(
                lambda x: color_map.get(str(x).strip().lower(), '#CCCCCC') if pd.notna(x) else '#CCCCCC'
            )
            
            # Create bar chart for top 10 colors
            fig_colors = px.bar(color_sales,
                               x='colour',
                               y='Gross_Amount',
                               title=f'Top 10 Colors by Gross Amount ({selected_year})',
                               labels={'colour': 'Color', 'Gross_Amount': 'Gross Amount (₹)'})
            
            # Update bar colors to match the actual color names
            fig_colors.update_traces(marker_color=color_sales['bar_color'].tolist())
            
            fig_colors.update_layout(
                xaxis_title="Color",
                yaxis_title="Gross Amount (₹)",
                bargap=0.2,
                height=600,
                showlegend=False
            )
            
            st.plotly_chart(fig_colors, use_container_width=True)
        
        # Add separator
        st.markdown("---")
        st.header("Top 10 Selling Products by SKU")
        
        # Group by SKU and calculate total sales
        sku_sales = filtered_df.groupby('sku').agg({
            'Gross_Amount': 'sum',
            'Quantity_Purchased': 'sum'
        }).reset_index()
        
        # Sort by gross amount and get top 10
        top_skus = sku_sales.sort_values('Gross_Amount', ascending=False).head(10)
        
        # Create bar chart for top 10 SKUs
        fig_sku = px.bar(top_skus,
                        x='sku',
                        y='Gross_Amount',
                        title=f'Top 10 Selling Products by SKU ({selected_year})',
                        labels={'sku': 'Product SKU', 'Gross_Amount': 'Gross Amount (₹)'},
                        color='Gross_Amount',
                        color_continuous_scale='Blues')
        
        fig_sku.update_layout(
            xaxis_title="Product SKU",
            yaxis_title="Gross Amount (₹)",
            bargap=0.2,
            height=600,
            showlegend=False,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig_sku, use_container_width=True)
    
    with tab2:
        st.header("📊 Comprehensive Product Analysis Dashboard")
        
        # Create sub-tabs for different analysis types
        analysis_tabs = st.tabs([
            "📦 Stock Analysis",
            "🏪 State Analytics", 
            "🏙️ City Analytics",
            "📢 Promotion Analysis",
            "📦 Order & Shipping",
            "🏢 B2B Analysis",
            "👗 Product Performance",
            "📈 Time Series"
        ])
        
        # ==================== TAB 0: Original Product Analysis ====================
        with analysis_tabs[0]:
            try:
                # Load the datasets separately for Product Analysis
                stock_report = pd.read_csv("new_stock_report.csv")
                international_data = pd.read_csv("new_international_sales_report.csv")
                
                # Verify required columns exist in stock_report
                required_stock_columns = ['sku', 'category', 'size', 'colour', 'stock']
                missing_stock_cols = [col for col in required_stock_columns if col not in stock_report.columns]
                if missing_stock_cols:
                    st.error(f"Missing columns in stock report: {', '.join(missing_stock_cols)}")
                else:
                    # Verify required columns exist in international_data
                    required_sales_columns = ['sku', 'Quantity_Purchased']
                    missing_sales_cols = [col for col in required_sales_columns if col not in international_data.columns]
                    if missing_sales_cols:
                        st.error(f"Missing columns in sales report: {', '.join(missing_sales_cols)}")
                    else:
                        # Create filters section
                        st.subheader("📊 Filter Products")
                        
                        # Get unique values for filters
                        categories = ['All'] + sorted(stock_report['category'].dropna().unique().tolist())
                        sizes = ['All'] + sorted(stock_report['size'].dropna().unique().tolist())
                        colors = ['All'] + sorted(stock_report['colour'].dropna().unique().tolist())
                        
                        # Create three columns for filters
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            selected_category = st.selectbox("Product Category", categories, key="orig_product_category")
                        
                        with col2:
                            selected_size = st.selectbox("Product Size", sizes, key="orig_product_size")
                        
                        with col3:
                            selected_color = st.selectbox("Product Color", colors, key="orig_product_color")
                        
                        # Apply filters to stock_report
                        filtered_stock = stock_report.copy()
                        
                        if selected_category != 'All':
                            filtered_stock = filtered_stock[filtered_stock['category'] == selected_category]
                        
                        if selected_size != 'All':
                            filtered_stock = filtered_stock[filtered_stock['size'] == selected_size]
                        
                        if selected_color != 'All':
                            filtered_stock = filtered_stock[filtered_stock['colour'] == selected_color]
                        
                        # Check if filtered data is empty
                        if len(filtered_stock) == 0:
                            st.warning("No products match the selected filters. Please adjust your selection.")
                        else:
                            # Add separator
                            st.markdown("---")
                            
                            # Section 1: Stock Analysis
                            st.subheader("📦 Stock Level Analysis")
                            
                            # Create two columns for stock charts
                            stock_col1, stock_col2 = st.columns(2)
                            
                            with stock_col1:
                                # Bar chart: Total Stock Level by Product Category
                                try:
                                    stock_by_category = filtered_stock.groupby('category')['stock'].sum().reset_index()
                                    stock_by_category = stock_by_category.sort_values('stock', ascending=False)
                                    
                                    fig_stock = px.bar(
                                        stock_by_category,
                                        x='category',
                                        y='stock',
                                        title='Total Stock Level by Category',
                                        labels={'category': 'Product Category', 'stock': 'Stock Level'},
                                        color='stock',
                                        color_continuous_scale='Viridis'
                                    )
                                    
                                    fig_stock.update_layout(
                                        xaxis_title="Product Category",
                                        yaxis_title="Total Stock Level",
                                        height=400,
                                        showlegend=False,
                                        xaxis_tickangle=-45
                                    )
                                    
                                    st.plotly_chart(fig_stock, use_container_width=True)
                                    
                                except Exception as e:
                                    st.error(f"Error creating stock level chart: {str(e)}")
                            
                            with stock_col2:
                                # Pie chart: Distribution of Product Size
                                try:
                                    size_distribution = filtered_stock.groupby('size').size().reset_index(name='count')
                                    
                                    fig_size = px.pie(
                                        size_distribution,
                                        values='count',
                                        names='size',
                                        title='Product Size Distribution',
                                        color_discrete_sequence=px.colors.qualitative.Pastel1
                                    )
                                    
                                    fig_size.update_traces(
                                        textposition='inside',
                                        textinfo='percent+label'
                                    )
                                    
                                    fig_size.update_layout(height=400)
                                    
                                    st.plotly_chart(fig_size, use_container_width=True)
                                    
                                except Exception as e:
                                    st.error(f"Error creating size distribution chart: {str(e)}")
                            
                            # Add separator
                            st.markdown("---")
                            
                            # Section 2: Top Selling Products Analysis
                            st.subheader("🏆 Top 10 Selling Products")
                            
                            try:
                                # Calculate top 10 products by total Quantity_Purchased
                                top_products = international_data.groupby('sku')['Quantity_Purchased'].sum().reset_index()
                                top_products = top_products.sort_values('Quantity_Purchased', ascending=False).head(10)
                                top_products.columns = ['Product_SKU', 'Total_Units_Sold']
                                
                                # Merge with stock report to get product details
                                top_products_details = pd.merge(
                                    top_products,
                                    stock_report[['sku', 'category', 'size', 'colour']].drop_duplicates(subset=['sku']),
                                    left_on='Product_SKU',
                                    right_on='sku',
                                    how='left'
                                )
                                
                                # Create bar chart for top 10 products
                                fig_top = px.bar(
                                    top_products,
                                    x='Product_SKU',
                                    y='Total_Units_Sold',
                                    title='Top 10 Best-Selling Products by Quantity Sold',
                                    labels={'Product_SKU': 'Product SKU', 'Total_Units_Sold': 'Total Units Sold'},
                                    color='Total_Units_Sold',
                                    color_continuous_scale='Teal',
                                    text='Total_Units_Sold'
                                )
                                
                                fig_top.update_traces(
                                    texttemplate='%{text:,.0f}',
                                    textposition='outside'
                                )
                                
                                fig_top.update_layout(
                                    xaxis_title="Product SKU",
                                    yaxis_title="Total Units Sold",
                                    height=500,
                                    showlegend=False,
                                    xaxis_tickangle=-45
                                )
                                
                                st.plotly_chart(fig_top, use_container_width=True)
                                
                                # Display data table with product details
                                st.subheader("📋 Top Selling Products - Detailed View")
                                
                                # Prepare display table
                                display_table = top_products_details[['Product_SKU', 'Total_Units_Sold', 'category', 'size', 'colour']].copy()
                                display_table.columns = ['Product SKU', 'Total Units Sold', 'Category', 'Size', 'Color']
                                
                                # Format numbers with commas
                                display_table['Total Units Sold'] = display_table['Total Units Sold'].apply(lambda x: f"{x:,.0f}")
                                
                                # Display table
                                st.dataframe(
                                    display_table,
                                    use_container_width=True,
                                    hide_index=True
                                )
                                
                                # Add summary metrics
                                st.markdown("---")
                                st.subheader("📈 Summary Metrics")
                                
                                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                                
                                with metric_col1:
                                    total_products = len(filtered_stock)
                                    st.metric("Total Products", f"{total_products:,}")
                                
                                with metric_col2:
                                    total_stock = filtered_stock['stock'].sum()
                                    st.metric("Total Stock", f"{total_stock:,.0f}")
                                
                                with metric_col3:
                                    total_sales = international_data['Quantity_Purchased'].sum()
                                    st.metric("Total Units Sold", f"{total_sales:,.0f}")
                                
                                with metric_col4:
                                    unique_categories = filtered_stock['category'].nunique()
                                    st.metric("Product Categories", f"{unique_categories}")
                                
                            except Exception as e:
                                st.error(f"Error analyzing top selling products: {str(e)}")
                                st.exception(e)
                
            except FileNotFoundError as e:
                st.error(f"Data file not found: {str(e)}")
                st.info("Please ensure both 'new_stock_report.csv' and 'new_international_sales_report.csv' are in the correct directory.")
            
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
                st.exception(e)
        
        # ==================== TAB 1: State Analytics ====================
        with analysis_tabs[1]:
            try:
                df_amazon = pd.read_csv("new_amazon_national_sales.csv")
                
                st.subheader("🛍️ Quantity, Sales & Avg Value State-wise Analytics")
                
                # Define numeric columns
                numeric_cols = ['quantity', 'sale', 'avg. value']
                df_amazon[numeric_cols] = df_amazon[numeric_cols].apply(pd.to_numeric, errors='coerce')
                df_amazon['state'] = df_amazon['state'].astype(str)
                
                # Sidebar filters
                st.sidebar.header("🔍 State Analytics Filters")
                
                selected_metrics = st.sidebar.multiselect(
                    "Select up to 3 Metrics",
                    options=numeric_cols,
                    default=['sale'],
                    max_selections=3,
                    key="state_metrics"
                )
                
                all_states = sorted(df_amazon['state'].dropna().unique())
                selected_states = st.sidebar.multiselect(
                    "Select States",
                    options=all_states,
                    default=all_states[:5],
                    key="state_filter"
                )
                
                filtered_df = df_amazon[df_amazon['state'].isin(selected_states)]
                
                # Range filters
                range_filters = {}
                for metric in selected_metrics:
                    col_values = pd.to_numeric(filtered_df[metric], errors='coerce').dropna()
                    if not col_values.empty:
                        min_val = int(col_values.min())
                        max_val = int(col_values.max())
                        if min_val == max_val:
                            max_val += 1
                        step = max((max_val - min_val) // 100, 1)
                        range_filters[metric] = st.sidebar.slider(
                            f"{metric} Range",
                            min_value=min_val,
                            max_value=max_val,
                            value=(min_val, max_val),
                            step=step,
                            key=f"state_{metric}_range"
                        )
                
                # Apply range filters
                for metric in range_filters:
                    min_val, max_val = range_filters[metric]
                    filtered_df = filtered_df[(filtered_df[metric] >= min_val) & (filtered_df[metric] <= max_val)]
                
                top_n = st.sidebar.number_input("Top N States", min_value=1, max_value=50, value=10, key="state_top_n")
                use_log = st.sidebar.checkbox("Use Log Scale", value=False, key="state_log")
                
                if not filtered_df.empty and selected_metrics:
                    grouped = filtered_df.groupby("state")[selected_metrics].sum().reset_index()
                    melted = pd.melt(grouped, id_vars="state", value_vars=selected_metrics,
                                   var_name="Metric", value_name="Value")
                    
                    if use_log:
                        melted = melted[melted["Value"] > 0]
                    
                    melted = melted.sort_values("Value", ascending=False).groupby("Metric").head(top_n)
                    
                    fig = px.bar(
                        melted,
                        x="state",
                        y="Value",
                        color="Metric",
                        barmode="group",
                        title="State vs Selected Metrics",
                        text_auto='.2s',
                        log_y=use_log
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data to display. Please adjust your filters.")
                    
            except Exception as e:
                st.error(f"Error in State Analytics: {str(e)}")
        
        # ==================== TAB 3: City Analytics ====================
        with analysis_tabs[2]:
            try:
                df_amazon = pd.read_csv("new_amazon_national_sales.csv")
                
                st.subheader("🏙️ Quantity, Sales & Avg Value City-wise Analytics")
                
                numeric_cols = ['quantity', 'sale', 'avg. value']
                df_amazon[numeric_cols] = df_amazon[numeric_cols].apply(pd.to_numeric, errors='coerce')
                
                st.sidebar.header("🔍 City Analytics Filters")
                
                all_states = sorted(df_amazon['state'].dropna().unique())
                selected_states_city = st.sidebar.multiselect(
                    "Select State(s)",
                    options=all_states,
                    default=all_states[:3],
                    key="city_state_filter"
                )
                
                filtered_state_df = df_amazon[df_amazon['state'].isin(selected_states_city)]
                filtered_state_df = filtered_state_df[filtered_state_df['city'].str.len() > 1]
                
                all_cities = sorted(filtered_state_df['city'].dropna().unique())
                selected_cities = st.sidebar.multiselect(
                    "Select City(s)",
                    options=all_cities,
                    default=all_cities[:10],
                    key="city_filter"
                )
                
                filtered_city_df = filtered_state_df[filtered_state_df['city'].isin(selected_cities)]
                
                selected_metrics_city = st.sidebar.multiselect(
                    "Select up to 3 Metrics",
                    options=numeric_cols,
                    default=['quantity', 'sale'],
                    max_selections=3,
                    key="city_metrics"
                )
                
                top_n_city = st.sidebar.number_input("Top N Cities", min_value=1, max_value=50, value=10, key="city_top_n")
                
                if not filtered_city_df.empty and selected_metrics_city:
                    grouped = filtered_city_df.groupby("city")[selected_metrics_city].sum().reset_index()
                    sort_metric = selected_metrics_city[0]
                    grouped = grouped.sort_values(by=sort_metric, ascending=False).head(top_n_city)
                    
                    melted = pd.melt(grouped, id_vars="city", value_vars=selected_metrics_city,
                                   var_name="Metric", value_name="Value")
                    
                    fig = px.bar(
                        melted,
                        x="city",
                        y="Value",
                        color="Metric",
                        barmode="group",
                        title=f"Top {top_n_city} Cities - Metrics",
                        text_auto='.2s'
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data to display. Please adjust your filters.")
                    
            except Exception as e:
                st.error(f"Error in City Analytics: {str(e)}")
        
        # ==================== TAB 4: Promotion Analysis ====================
        with analysis_tabs[3]:
            try:
                df_amazon = pd.read_csv("new_amazon_national_sales.csv")
                
                st.subheader("📢 Promotion Analysis")
                
                # State-based Promotion Analysis
                st.markdown("### 🏪 Promotion by State")
                
                df_amazon['Promotion_ID_Count'] = df_amazon['Promotion_ID_Count'].astype(str)
                df_amazon['state'] = df_amazon['state'].astype(str)
                
                st.sidebar.header("🔍 Promotion Filters")
                
                all_states_promo = sorted(df_amazon['state'].dropna().unique())
                selected_states_promo = st.sidebar.multiselect(
                    "Select States (Promo)",
                    options=all_states_promo,
                    default=all_states_promo[:10],
                    key="promo_state_filter"
                )
                
                filtered_df_promo = df_amazon[df_amazon['state'].isin(selected_states_promo)]
                grouped_promo = filtered_df_promo.groupby("state")["Promotion_ID_Count"].nunique().reset_index(name="Promotion_Count")
                
                if not grouped_promo.empty:
                    top_n_promo = st.sidebar.number_input("Top N States by Promotion", 1, 50, 10, key="promo_top_n")
                    grouped_promo = grouped_promo.sort_values("Promotion_Count", ascending=False).head(top_n_promo)
                    
                    fig_promo_state = px.bar(
                        grouped_promo,
                        x="state",
                        y="Promotion_Count",
                        title="Top States by Promotion Count",
                        text_auto=True,
                        color='Promotion_Count',
                        color_continuous_scale='Plasma'
                    )
                    fig_promo_state.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig_promo_state, use_container_width=True)
                
                # City-based Promotion Analysis
                st.markdown("---")
                st.markdown("### 🏙️ Promotion by City")
                
                df_promo_city = df_amazon.copy()
                df_promo_city = df_promo_city[df_promo_city['city'].str.len() > 1]
                df_promo_city = df_promo_city.dropna(subset=['city', 'state'])
                
                cities_promo = sorted(df_promo_city['city'].unique())
                selected_cities_promo = st.sidebar.multiselect(
                    "Select Cities (Promo)",
                    options=cities_promo,
                    default=cities_promo[:10],
                    key="promo_city_filter"
                )
                
                filtered_city_promo = df_promo_city[df_promo_city['city'].isin(selected_cities_promo)]
                
                min_y_promo = st.sidebar.number_input("Min Promotion Count", min_value=0, value=5, key="promo_min_y")
                top_n_city_promo = st.sidebar.number_input("Top N Cities (Promo)", min_value=1, max_value=100, value=10, key="promo_city_top_n")
                
                grouped_city_promo = filtered_city_promo.groupby("city")["Promotion_ID_Count"].nunique().reset_index(name='Promotion_Count')
                grouped_city_promo = grouped_city_promo[grouped_city_promo['Promotion_Count'] >= min_y_promo]
                grouped_city_promo = grouped_city_promo.sort_values(by="Promotion_Count", ascending=False).head(top_n_city_promo)
                
                if not grouped_city_promo.empty:
                    fig_promo_city = px.bar(
                        grouped_city_promo,
                        x="city",
                        y="Promotion_Count",
                        title="Top Cities by Promotion Count",
                        text_auto=True,
                        color='Promotion_Count',
                        color_continuous_scale='Sunset'
                    )
                    fig_promo_city.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig_promo_city, use_container_width=True)
                else:
                    st.warning("No data available for selected filters.")
                    
            except Exception as e:
                st.error(f"Error in Promotion Analysis: {str(e)}")
        
        # ==================== TAB 5: Order & Shipping ====================
        with analysis_tabs[4]:
            try:
                df_amazon = pd.read_csv("new_amazon_national_sales.csv")
                
                st.subheader("📦 Order Status & Shipping Analysis")
                
                df_clean = df_amazon.dropna(subset=["city", "state", "Order_Status", "shipping_level"])
                df_clean = df_clean[~df_clean['city'].str.fullmatch(r'^[A-Z]$', na=False)]
                
                st.sidebar.header("🔍 Order & Shipping Filters")
                
                filter_type = st.sidebar.radio("Filter By", ["State", "City"], key="order_filter_type")
                
                states_order = sorted(df_clean['state'].dropna().unique())
                selected_states_order = st.sidebar.multiselect("Select States (Order)", states_order, key="order_state_filter")
                
                if selected_states_order:
                    filtered_cities_order = sorted(df_clean[df_clean['state'].isin(selected_states_order)]['city'].dropna().unique())
                else:
                    filtered_cities_order = sorted(df_clean['city'].dropna().unique())
                
                selected_cities_order = st.sidebar.multiselect("Select Cities (Order)", filtered_cities_order, key="order_city_filter")
                
                metric_type = st.sidebar.radio("Select Metric", ["Count", "Percentage"], key="order_metric")
                chart_type_order = st.sidebar.selectbox("Chart Type", ['Bar', 'Pie', 'Line'], key="order_chart")
                
                if filter_type == "State":
                    group_col = "state"
                    df_clean = df_clean[df_clean['state'].isin(selected_states_order)] if selected_states_order else df_clean
                else:
                    group_col = "city"
                    df_clean = df_clean[df_clean['city'].isin(selected_cities_order)] if selected_cities_order else df_clean
                
                if metric_type == "Count":
                    grouped_order = df_clean.groupby([group_col, 'Order_Status']).size().reset_index(name='Count')
                    y_col = 'Count'
                else:
                    grouped_order = df_clean.groupby([group_col, 'Order_Status']).size().reset_index(name='Count')
                    grouped_order['Percentage'] = grouped_order.groupby(group_col)['Count'].transform(lambda x: x / x.sum() * 100)
                    y_col = 'Percentage'
                
                if not grouped_order.empty:
                    if chart_type_order == "Bar":
                        fig_order = px.bar(
                            grouped_order,
                            x=group_col,
                            y=y_col,
                            color='Order_Status',
                            title=f"{y_col} by {group_col} and Order Status",
                            barmode='stack',
                            text_auto='.2f' if metric_type == "Percentage" else True
                        )
                        fig_order.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig_order, use_container_width=True)
                    
                    elif chart_type_order == "Pie":
                        pie_data_order = grouped_order.groupby('Order_Status')[y_col].sum().reset_index()
                        fig_order = px.pie(
                            pie_data_order,
                            names='Order_Status',
                            values=y_col,
                            title=f"Order Status Distribution",
                            hole=0.3
                        )
                        st.plotly_chart(fig_order, use_container_width=True)
                    
                    elif chart_type_order == "Line":
                        fig_order = px.line(
                            grouped_order,
                            x=group_col,
                            y=y_col,
                            color='Order_Status',
                            title=f"Order Status Trend",
                            markers=True
                        )
                        st.plotly_chart(fig_order, use_container_width=True)
                else:
                    st.warning("No data available for selected filters.")
                    
            except Exception as e:
                st.error(f"Error in Order & Shipping Analysis: {str(e)}")
        
        # ==================== TAB 6: B2B Analysis ====================
        with analysis_tabs[5]:
            try:
                df_amazon = pd.read_csv("new_amazon_national_sales.csv")
                
                st.subheader("🏢 B2B Distribution Analysis")
                
                df_b2b = df_amazon.dropna(subset=['state', 'city', 'b2b'])
                df_b2b = df_b2b[df_b2b['city'].str.len() > 1]
                
                st.sidebar.header("🔍 B2B Filters")
                
                analysis_type = st.sidebar.radio("Analysis Type", ['B2B by State', 'B2B by City'], key="b2b_type")
                
                if analysis_type == "B2B by State":
                    state_b2b = df_b2b.groupby(['state', 'b2b']).size().reset_index(name='Count')
                    state_total = df_b2b.groupby('state').size().reset_index(name='Total')
                    state_b2b = state_b2b.merge(state_total, on='state')
                    state_b2b['Percent'] = (state_b2b['Count'] / state_b2b['Total']) * 100
                    
                    fig_b2b = px.bar(
                        state_b2b,
                        x='state',
                        y='Percent',
                        color='b2b',
                        barmode='stack',
                        title="B2B % Distribution by State",
                        text_auto='.2f'
                    )
                    fig_b2b.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig_b2b, use_container_width=True)
                
                else:
                    states_b2b = sorted(df_b2b['state'].unique())
                    selected_states_b2b = st.sidebar.multiselect("Select States (B2B)", states_b2b, default=states_b2b[:5], key="b2b_state_filter")
                    
                    filtered_df_b2b = df_b2b[df_b2b['state'].isin(selected_states_b2b)]
                    
                    cities_b2b = sorted(filtered_df_b2b['city'].unique())
                    selected_cities_b2b = st.sidebar.multiselect("Select Cities (B2B)", cities_b2b, default=cities_b2b[:10], key="b2b_city_filter")
                    
                    top_n_b2b = st.sidebar.number_input("Top N Cities (B2B)", 1, 100, 10, key="b2b_top_n")
                    
                    df_city_b2b = filtered_df_b2b[filtered_df_b2b['city'].isin(selected_cities_b2b)]
                    top_cities_b2b = df_city_b2b['city'].value_counts().head(top_n_b2b).index
                    df_city_b2b = df_city_b2b[df_city_b2b['city'].isin(top_cities_b2b)]
                    
                    if not df_city_b2b.empty:
                        city_b2b = df_city_b2b.groupby(['city', 'b2b']).size().reset_index(name='Count')
                        city_total = df_city_b2b.groupby('city').size().reset_index(name='Total')
                        city_b2b = city_b2b.merge(city_total, on='city')
                        city_b2b['Percent'] = (city_b2b['Count'] / city_b2b['Total']) * 100
                        
                        fig_b2b_city = px.bar(
                            city_b2b,
                            x='city',
                            y='Percent',
                            color='b2b',
                            barmode='stack',
                            title="B2B % Distribution by City",
                            text_auto='.2f'
                        )
                        fig_b2b_city.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig_b2b_city, use_container_width=True)
                    else:
                        st.warning("No data for selected filters.")
                        
            except Exception as e:
                st.error(f"Error in B2B Analysis: {str(e)}")
        
        # ==================== TAB 7: Product Performance ====================
        with analysis_tabs[6]:
            try:
                df_amazon = pd.read_csv("new_amazon_national_sales.csv")
                
                st.subheader("👗 Product Category & Size Performance")
                
                df_product = df_amazon.dropna(subset=['state', 'category', 'size', 'quantity', 'sale'])
                df_product = df_product[~df_product['state'].str.fullmatch(r"[A-Za-z]", na=False)]
                
                st.sidebar.header("🔍 Product Performance Filters")
                
                metric_product = st.sidebar.selectbox("Select Metric", ["quantity", "sale"], key="product_metric")
                
                states_product = sorted(df_product['state'].dropna().unique())
                selected_states_product = st.sidebar.multiselect("Select States (Product)", states_product, default=states_product[:5], key="product_state_filter")
                
                df_filtered_product = df_product[df_product['state'].isin(selected_states_product)]
                
                top_n_product = st.sidebar.number_input("Top N States (Product)", min_value=1, max_value=50, value=10, key="product_top_n")
                
                # Category Analysis
                st.markdown("### 📊 By Product Category")
                grouped_cat = df_filtered_product.groupby(['state', 'category'])[metric_product].sum().reset_index()
                grouped_cat = grouped_cat.sort_values(by=metric_product, ascending=False).groupby('state').head(top_n_product)
                
                fig_cat = px.bar(grouped_cat, x="state", y=metric_product, color="category",
                               title=f"{metric_product} by Product Category and State", barmode="group")
                fig_cat.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_cat, use_container_width=True)
                
                # Percentage by Category
                df_cat_pct = grouped_cat.copy()
                df_cat_pct["Percentage"] = df_cat_pct.groupby("state")[metric_product].transform(lambda x: x / x.sum() * 100)
                fig_pct_cat = px.bar(df_cat_pct, x="state", y="Percentage", color="category",
                                   title=f"% {metric_product} by Product Category", barmode="stack")
                fig_pct_cat.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_pct_cat, use_container_width=True)
                
                # Size Analysis
                st.markdown("---")
                st.markdown("### 📏 By Product Size")
                grouped_size = df_filtered_product.groupby(['state', 'size'])[metric_product].sum().reset_index()
                grouped_size = grouped_size.sort_values(by=metric_product, ascending=False).groupby('state').head(top_n_product)
                
                fig_size = px.bar(grouped_size, x="state", y=metric_product, color="size",
                                title=f"{metric_product} by Product Size and State", barmode="group")
                fig_size.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_size, use_container_width=True)
                
                # Percentage by Size
                df_size_pct = grouped_size.copy()
                df_size_pct["Percentage"] = df_size_pct.groupby("state")[metric_product].transform(lambda x: x / x.sum() * 100)
                fig_pct_size = px.bar(df_size_pct, x="state", y="Percentage", color="size",
                                    title=f"% {metric_product} by Product Size", barmode="stack")
                fig_pct_size.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_pct_size, use_container_width=True)
                
                # Category vs Size Analysis
                st.markdown("---")
                st.markdown("### 🔄 Category vs Size Analysis")
                
                constant_col = st.selectbox("Group by", ["category", "size"], key="product_group_by")
                dynamic_col = "size" if constant_col == "category" else "category"
                
                grouped_cross = df_filtered_product.groupby([constant_col, dynamic_col])[metric_product].sum().reset_index()
                options = grouped_cross[constant_col].unique().tolist()
                selected_group = st.selectbox(f"Select {constant_col}", options, key="product_selected_group")
                
                filtered_cross = grouped_cross[grouped_cross[constant_col] == selected_group]
                
                fig_cross = px.bar(
                    filtered_cross,
                    x=dynamic_col,
                    y=metric_product,
                    title=f"{selected_group} - {dynamic_col}: {metric_product}",
                    color_discrete_sequence=["#1f77b4"]
                )
                fig_cross.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_cross, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error in Product Performance: {str(e)}")
        
        # ==================== TAB 8: Time Series ====================
        with analysis_tabs[7]:
            try:
                df_amazon = pd.read_csv("new_amazon_national_sales.csv")
                
                st.subheader("📈 Time Series Analysis")
                
                # Convert date
                df_amazon['date'] = pd.to_datetime(df_amazon['date'], errors='coerce')
                df_time = df_amazon.dropna(subset=['date'])
                
                # Extract month info
                df_time['Month'] = df_time['date'].dt.month
                df_time['MonthName'] = df_time['date'].dt.strftime('%B')
                df_time['Year'] = df_time['date'].dt.year
                
                # Month order
                month_order = {
                    'January': 1, 'February': 2, 'March': 3, 'April': 4,
                    'May': 5, 'June': 6, 'July': 7, 'August': 8,
                    'September': 9, 'October': 10, 'November': 11, 'December': 12
                }
                df_time['MonthOrder'] = df_time['MonthName'].map(month_order)
                
                # Convert numeric
                df_time['sale'] = pd.to_numeric(df_time['sale'], errors='coerce')
                df_time['quantity'] = pd.to_numeric(df_time['quantity'], errors='coerce')
                df_time['avg. value'] = pd.to_numeric(df_time['avg. value'], errors='coerce')
                
                # Aggregate by month
                monthly_agg = df_time.groupby(['MonthOrder', 'MonthName'])[['quantity', 'sale', 'avg. value']].sum().reset_index()
                monthly_agg = monthly_agg.sort_values('MonthOrder')
                
                # Line Chart
                st.markdown("### 📊 Monthly Trends")
                fig_line_time = px.line(
                    monthly_agg,
                    x='MonthName',
                    y=['quantity', 'sale', 'avg. value'],
                    title="Monthly Trends: Quantity, Sales & Avg Value",
                    markers=True,
                    color_discrete_sequence=px.colors.qualitative.Set1
                )
                fig_line_time.update_layout(
                    xaxis_title="Month",
                    yaxis_title="Value",
                    xaxis=dict(categoryorder='array', categoryarray=list(month_order.keys()))
                )
                st.plotly_chart(fig_line_time, use_container_width=True)
                
                # Pie Chart
                st.markdown("---")
                st.markdown("### 🥧 Monthly Distribution")
                metric_time = st.selectbox("Select Metric for Pie", ['quantity', 'sale', 'avg. value'], key="time_pie_metric")
                
                pie_df = monthly_agg[['MonthName', metric_time]]
                fig_pie_time = px.pie(
                    pie_df,
                    names='MonthName',
                    values=metric_time,
                    title=f"Monthly Distribution of {metric_time}",
                    color_discrete_sequence=px.colors.qualitative.Pastel1
                )
                st.plotly_chart(fig_pie_time, use_container_width=True)
                
                # Product Category/Size by Month
                st.markdown("---")
                st.markdown("### 📅 Product Analysis by Month")
                
                months = sorted(df_time['MonthName'].unique(), key=lambda m: month_order[m])
                selected_months = st.multiselect("Select Months", options=months, default=months[:3], key="time_months")
                dimension_time = st.selectbox("Select Dimension", ['category', 'size'], key="time_dimension")
                metric_time_prod = st.selectbox("Select Metric", ['quantity', 'sale', 'avg. value'], key="time_product_metric")
                
                filtered_df_time = df_time[df_time['MonthName'].isin(selected_months)]
                
                # Line graph
                line_data_time = filtered_df_time.groupby(['MonthOrder', 'MonthName', dimension_time])[metric_time_prod].sum().reset_index()
                line_data_time = line_data_time.sort_values('MonthOrder')
                
                fig_line_prod = px.line(
                    line_data_time,
                    x='MonthName',
                    y=metric_time_prod,
                    color=dimension_time,
                    markers=True,
                    title=f"{metric_time_prod} over Months by {dimension_time}"
                )
                st.plotly_chart(fig_line_prod, use_container_width=True)
                
                # Percentage stacked bar
                bar_data_time = filtered_df_time.groupby([dimension_time, 'MonthName'])[metric_time_prod].sum().reset_index()
                bar_data_time['Percent'] = bar_data_time.groupby('MonthName')[metric_time_prod].transform(lambda x: 100 * x / x.sum())
                
                fig_bar_time = px.bar(
                    bar_data_time,
                    x='MonthName',
                    y='Percent',
                    color=dimension_time,
                    title=f"% Distribution of {metric_time_prod} by {dimension_time}",
                    barmode='stack'
                )
                st.plotly_chart(fig_bar_time, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error in Time Series Analysis: {str(e)}")
    
    with tab3:
        st.header("📦 Inventory Stock Management")
        
        try:
            # Load stock and sales data
            stock_df = pd.read_csv("new_stock_report.csv")
            sales_df = pd.read_csv("new_international_sales_report.csv")
            
            # Convert sale date to datetime
            sales_df['date'] = pd.to_datetime(sales_df['date'], format='%d-%m-%Y', errors='coerce')
            
            # ==================== STOCK LEVEL OVERVIEW ====================
            st.subheader("📊 Stock Level Overview")
            
            # Categorize stock levels
            def categorize_stock(level):
                if level <= 10:
                    return "Low"
                elif level <= 50:
                    return "Medium"
                else:
                    return "High"
            
            stock_df['Stock_Category'] = stock_df['stock'].apply(categorize_stock)
            
            # Create pie chart with pastel colors
            stock_distribution = stock_df['Stock_Category'].value_counts().reset_index()
            stock_distribution.columns = ['Category', 'Count']
            
            fig_stock_pie = px.pie(
                stock_distribution,
                values='Count',
                names='Category',
                title='Stock Level Distribution',
                color='Category',
                color_discrete_map={
                    'Low': '#FFB6C1',      # Light Pink
                    'Medium': '#FFE4B5',   # Moccasin
                    'High': '#B0E0E6'      # Powder Blue
                }
            )
            fig_stock_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_stock_pie, use_container_width=True)
            
            # ==================== LOW STOCK ALERT SECTION ====================
            st.markdown("---")
            st.subheader("⚠️ Low Stock Alert")
            
            # Identify low stock items (stock <= 10)
            low_stock = stock_df[stock_df['stock'] <= 10].copy()
            
            if len(low_stock) > 0:
                st.warning(f"🚨 **{len(low_stock)} items** have critically low stock levels (≤10 units)")
                
                # Calculate sales metrics for low stock items
                if not sales_df.empty:
                    sales_metrics = []
                    
                    for sku in low_stock['sku'].unique():
                        sku_sales = sales_df[sales_df['sku'] == sku].copy()
                        
                        if len(sku_sales) > 0:
                            # Sort by date
                            sku_sales = sku_sales.sort_values('date')
                            
                            # Days since last sale
                            last_sale = sku_sales['date'].max()
                            days_since_last = (pd.Timestamp.now() - last_sale).days if pd.notna(last_sale) else None
                            
                            # Calculate average days between sales
                            if len(sku_sales) > 1:
                                date_diffs = sku_sales['date'].diff().dt.days.dropna()
                                avg_days_between = date_diffs.mean() if len(date_diffs) > 0 else None
                            else:
                                avg_days_between = None
                            
                            # Sale count
                            sale_count = len(sku_sales)
                            total_qty = sku_sales['Quantity_Purchased'].sum()
                            
                            sales_metrics.append({
                                'sku': sku,
                                'Days_Since_Last_Sale': days_since_last,
                                'Avg_Days_Between_Sales': avg_days_between,
                                'Sale_Count': sale_count,
                                'Total_Quantity_Sold': total_qty
                            })
                        else:
                            sales_metrics.append({
                                'sku': sku,
                                'Days_Since_Last_Sale': None,
                                'Avg_Days_Between_Sales': None,
                                'Sale_Count': 0,
                                'Total_Quantity_Sold': 0
                            })
                    
                    # Merge sales metrics with low stock data
                    metrics_df = pd.DataFrame(sales_metrics)
                    low_stock = low_stock.merge(metrics_df, on='sku', how='left')
                    
                    # Classify reorder priority
                    def classify_priority(row):
                        if row['Sale_Count'] > 10 and (row['Days_Since_Last_Sale'] or 0) < 30:
                            return "High"
                        elif row['Sale_Count'] > 5:
                            return "Medium"
                        else:
                            return "Low"
                    
                    low_stock['Reorder_Priority'] = low_stock.apply(classify_priority, axis=1)
                    
                    # Calculate recommended reorder quantity for high priority items
                    def calculate_reorder_qty(row):
                        if row['Reorder_Priority'] == "High" and row['Sale_Count'] > 0:
                            # Frequency-based: estimate monthly demand
                            if row['Avg_Days_Between_Sales'] and row['Avg_Days_Between_Sales'] > 0:
                                monthly_demand = (30 / row['Avg_Days_Between_Sales']) * (row['Total_Quantity_Sold'] / row['Sale_Count'])
                                return int(monthly_demand * 2)  # 2 months buffer
                            else:
                                return int(row['Total_Quantity_Sold'] / row['Sale_Count'] * 30)  # Monthly estimate
                        return 0
                    
                    low_stock['Recommended_Reorder_Qty'] = low_stock.apply(calculate_reorder_qty, axis=1)
                
                # Display low stock dataframe
                display_cols = ['sku', 'design_no', 'category', 'colour', 'stock']
                if 'Reorder_Priority' in low_stock.columns:
                    display_cols.extend(['Reorder_Priority', 'Sale_Count', 'Days_Since_Last_Sale', 'Recommended_Reorder_Qty'])
                
                st.dataframe(low_stock[display_cols].sort_values('stock'), use_container_width=True)
                
                # Show high priority items separately
                if 'Reorder_Priority' in low_stock.columns:
                    high_priority = low_stock[low_stock['Reorder_Priority'] == 'High']
                    if len(high_priority) > 0:
                        st.error(f"🔥 **{len(high_priority)} HIGH PRIORITY items** need immediate reordering!")
                        st.dataframe(
                            high_priority[['sku', 'design_no', 'category', 'colour', 'stock', 'Sale_Count', 'Recommended_Reorder_Qty']],
                            use_container_width=True
                        )
            else:
                st.success("✅ No items with critically low stock levels")
            
            # ==================== OVERSTOCKED PRODUCTS ====================
            st.markdown("---")
            st.subheader("📈 Overstocked Products Analysis")
            
            # Calculate total sales by SKU
            if not sales_df.empty:
                total_sales = sales_df.groupby('sku')['Quantity_Purchased'].sum().reset_index()
                total_sales.columns = ['sku', 'Total_Sales']
                
                # Merge with stock data
                stock_sales = stock_df.merge(total_sales, on='sku', how='left')
                stock_sales['Total_Sales'] = stock_sales['Total_Sales'].fillna(0)
                
                # Calculate Stock to Sales Ratio
                stock_sales['Stock_to_Sales_Ratio'] = stock_sales['stock'] / (stock_sales['Total_Sales'] + 1)
                
                # Identify overstocked products (stock > 50 and ratio > 5)
                overstocked = stock_sales[(stock_sales['stock'] > 50) & (stock_sales['Stock_to_Sales_Ratio'] > 5)].copy()
                
                if len(overstocked) > 0:
                    st.warning(f"⚠️ **{len(overstocked)} products** appear to be overstocked")
                    
                    # Add days since last sale
                    last_sale_dates = sales_df.groupby('sku')['date'].max().reset_index()
                    last_sale_dates.columns = ['sku', 'Last_Sale_Date']
                    overstocked = overstocked.merge(last_sale_dates, on='sku', how='left')
                    overstocked['Days_Since_Last_Sale'] = (pd.Timestamp.now() - overstocked['Last_Sale_Date']).dt.days
                    
                    # Add actionable recommendations
                    def get_recommendation(row):
                        if row['Days_Since_Last_Sale'] > 180 and row['Total_Sales'] < 5:
                            return "Consider discontinuing"
                        elif row['Days_Since_Last_Sale'] > 90:
                            return "Urgent discount needed"
                        elif row['Stock_to_Sales_Ratio'] > 10:
                            return "Promote heavily"
                        else:
                            return "Monitor closely"
                    
                    overstocked['Recommendation'] = overstocked.apply(get_recommendation, axis=1)
                    
                    # Display overstocked data
                    st.dataframe(
                        overstocked[['sku', 'design_no', 'category', 'colour', 'stock', 'Total_Sales', 
                                   'Stock_to_Sales_Ratio', 'Days_Since_Last_Sale', 'Recommendation']].round(2),
                        use_container_width=True
                    )
                    
                    # Scatter plot: Stock vs Sales
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig_scatter = px.scatter(
                            overstocked,
                            x='Total_Sales',
                            y='stock',
                            color='Recommendation',
                            hover_data=['sku', 'category', 'colour'],
                            title='Stock Level vs Total Sales (Overstocked Items)',
                            labels={'Total_Sales': 'Total Sales', 'stock': 'Stock Level'},
                            color_discrete_map={
                                'Consider discontinuing': '#FF6B6B',
                                'Urgent discount needed': '#FFA07A',
                                'Promote heavily': '#FFD93D',
                                'Monitor closely': '#A8E6CF'
                            }
                        )
                        st.plotly_chart(fig_scatter, use_container_width=True)
                    
                    with col2:
                        # Treemap: Category-wise overstock
                        category_overstock = overstocked.groupby('category').agg({
                            'stock': 'sum',
                            'sku': 'count'
                        }).reset_index()
                        category_overstock.columns = ['Category', 'Total_Stock', 'Product_Count']
                        
                        fig_treemap = px.treemap(
                            category_overstock,
                            path=['Category'],
                            values='Total_Stock',
                            title='Category-wise Overstock Distribution',
                            color='Product_Count',
                            color_continuous_scale='Reds'
                        )
                        st.plotly_chart(fig_treemap, use_container_width=True)
                else:
                    st.success("✅ No significantly overstocked products detected")
            else:
                st.info("ℹ️ Sales data not available for overstock analysis")
            
            # ==================== SUMMARY VISUALS ====================
            st.markdown("---")
            st.subheader("📊 Inventory Summary")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Total stock by category
                total_stock_category = stock_df.groupby('category')['stock'].sum().reset_index()
                total_stock_category = total_stock_category.sort_values('stock', ascending=False)
                
                fig_cat_bar = px.bar(
                    total_stock_category,
                    x='category',
                    y='stock',
                    title='Total Stock by Category',
                    labels={'category': 'Category', 'stock': 'Total Stock'},
                    color='stock',
                    color_continuous_scale='Blues'
                )
                fig_cat_bar.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_cat_bar, use_container_width=True)
            
            with col2:
                # Total stock by color (top 15)
                total_stock_color = stock_df.groupby('colour')['stock'].sum().reset_index()
                total_stock_color = total_stock_color.sort_values('stock', ascending=False).head(15)
                
                fig_color_bar = px.bar(
                    total_stock_color,
                    x='colour',
                    y='stock',
                    title='Total Stock by Color (Top 15)',
                    labels={'colour': 'Color', 'stock': 'Total Stock'},
                    color='stock',
                    color_continuous_scale='Viridis'
                )
                fig_color_bar.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_color_bar, use_container_width=True)
            
            # Add third row for size distribution
            st.markdown("---")
            
            # Total stock by size
            total_stock_size = stock_df.groupby('size')['stock'].sum().reset_index()
            
            # Sort by stock in descending order
            total_stock_size = total_stock_size.sort_values('stock', ascending=False)
            
            fig_size_bar = px.bar(
                total_stock_size,
                x='size',
                y='stock',
                title='Total Stock Level by Size',
                labels={'size': 'Size', 'stock': 'Total Stock'},
                color='stock',
                color_continuous_scale='Oranges'
            )
            fig_size_bar.update_layout(xaxis_tickangle=0, height=500)
            st.plotly_chart(fig_size_bar, use_container_width=True)
            
            # Key Metrics Summary
            st.markdown("---")
            st.subheader("📋 Key Metrics")
            
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                total_stock = stock_df['stock'].sum()
                st.metric("Total Stock Units", f"{total_stock:,.0f}")
            
            with metric_col2:
                avg_stock = stock_df['stock'].mean()
                st.metric("Average Stock per SKU", f"{avg_stock:.1f}")
            
            with metric_col3:
                low_stock_count = len(stock_df[stock_df['stock'] <= 10])
                st.metric("Low Stock Items", low_stock_count)
            
            with metric_col4:
                unique_skus = stock_df['sku'].nunique()
                st.metric("Total SKUs", unique_skus)
            
        except Exception as e:
            st.error(f"Error in Inventory Stock Management: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
    with tab4:
        st.header("🔄 Product Return Analysis")
        
        try:
            # Load data files
            amazon_df = pd.read_csv("new_amazon_national_sales.csv")
            stock_df = pd.read_csv("new_stock_report.csv")
            
            # Clean column names (remove extra spaces)
            amazon_df.columns = amazon_df.columns.str.strip()
            stock_df.columns = stock_df.columns.str.strip()
            
            # Convert order date to datetime
            amazon_df['date'] = pd.to_datetime(amazon_df['date'], format='%Y-%m-%d', errors='coerce')
            
            # Extract month and year for trend analysis
            amazon_df['Month'] = amazon_df['date'].dt.to_period('M').astype(str)
            amazon_df['Year'] = amazon_df['date'].dt.year
            
            # Identify returns/cancellations (case-insensitive)
            amazon_df['is_return'] = amazon_df['Order_Status'].str.lower().str.contains('cancelled|returned', na=False)
            
            # Calculate return metrics by SKU
            sku_metrics = amazon_df.groupby('sku').agg({
                'Order_ID': 'count',  # Total orders
                'is_return': 'sum'     # Total returns
            }).reset_index()
            sku_metrics.columns = ['sku', 'total_orders', 'total_returns']
            
            # Calculate return rate
            sku_metrics['return_rate'] = (sku_metrics['total_returns'] / sku_metrics['total_orders']) * 100
            sku_metrics['return_rate'] = sku_metrics['return_rate'].fillna(0)
            
            # Merge with stock data for category and stock level info
            analysis_df = sku_metrics.merge(stock_df, on='sku', how='left')
            
            # Clean null values
            analysis_df = analysis_df.dropna(subset=['category', 'stock'])
            
            # ==================== DASHBOARD HEADER ====================
            st.subheader("📈 Return Rate Analytics")
            
            # Key Metrics
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                total_orders = amazon_df['Order_ID'].nunique()
                st.metric("Total Orders", f"{total_orders:,}")
            
            with metric_col2:
                total_returns = amazon_df[amazon_df['is_return']]['Order_ID'].count()
                st.metric("Total Returns", f"{total_returns:,}")
            
            with metric_col3:
                overall_return_rate = (total_returns / len(amazon_df)) * 100
                st.metric("Overall Return Rate", f"{overall_return_rate:.2f}%")
            
            with metric_col4:
                high_return_products = len(analysis_df[analysis_df['return_rate'] >= 90])
                st.metric("High Return Products (≥90%)", high_return_products)
            
            # ==================== 1. PRODUCTS WITH ≥90% RETURN RATE ====================
            st.markdown("---")
            st.subheader("🚨 Products with High Return Rate (≥90%)")
            
            high_return_df = analysis_df[analysis_df['return_rate'] >= 90].copy()
            
            if len(high_return_df) > 0:
                # Sort by return rate descending
                high_return_df = high_return_df.sort_values('return_rate', ascending=False).head(20)
                
                fig_high_return = px.bar(
                    high_return_df,
                    x='sku',
                    y='return_rate',
                    title='Top 20 Products with ≥90% Return Rate',
                    labels={'sku': 'Product SKU', 'return_rate': 'Return Rate (%)'},
                    color='return_rate',
                    color_continuous_scale='Reds',
                    hover_data=['category', 'total_orders', 'total_returns']
                )
                fig_high_return.update_layout(xaxis_tickangle=-45, height=500)
                st.plotly_chart(fig_high_return, use_container_width=True)
                
                # Show data table
                st.dataframe(
                    high_return_df[['sku', 'category', 'total_orders', 'total_returns', 'return_rate', 'stock']].round(2),
                    use_container_width=True
                )
            else:
                st.success("✅ No products with return rate ≥90%")
            
            # ==================== 2. PIE CHART - RETURN RATE DISTRIBUTION ====================
            st.markdown("---")
            st.subheader("📊 Return Rate Distribution by Range")
            
            # Categorize products by return rate ranges
            def categorize_return_rate(rate):
                if rate <= 10:
                    return "0-10%"
                elif rate <= 20:
                    return "10-20%"
                elif rate <= 30:
                    return "20-30%"
                elif rate <= 40:
                    return "30-40%"
                elif rate <= 50:
                    return "40-50%"
                elif rate <= 60:
                    return "50-60%"
                elif rate <= 70:
                    return "60-70%"
                elif rate <= 80:
                    return "70-80%"
                elif rate <= 90:
                    return "80-90%"
                else:
                    return "90-100%"
            
            analysis_df['return_rate_range'] = analysis_df['return_rate'].apply(categorize_return_rate)
            
            # Count products in each range
            range_distribution = analysis_df['return_rate_range'].value_counts().reset_index()
            range_distribution.columns = ['Range', 'Count']
            
            # Sort by range order
            range_order = ["0-10%", "10-20%", "20-30%", "30-40%", "40-50%", 
                          "50-60%", "60-70%", "70-80%", "80-90%", "90-100%"]
            range_distribution['Range'] = pd.Categorical(range_distribution['Range'], categories=range_order, ordered=True)
            range_distribution = range_distribution.sort_values('Range')
            
            fig_pie = px.pie(
                range_distribution,
                values='Count',
                names='Range',
                title='Product Distribution by Return Rate Range',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # ==================== 3. AVERAGE RETURN RATE BY CATEGORY ====================
            st.markdown("---")
            st.subheader("📦 Average Return Rate by Product Category")
            
            category_return = analysis_df.groupby('category')['return_rate'].mean().reset_index()
            category_return = category_return.sort_values('return_rate', ascending=False)
            
            fig_category = px.bar(
                category_return,
                x='category',
                y='return_rate',
                title='Average Return Rate by Category',
                labels={'category': 'Product Category', 'return_rate': 'Average Return Rate (%)'},
                color='return_rate',
                color_continuous_scale='Oranges'
            )
            fig_category.update_layout(xaxis_tickangle=-45, height=500)
            st.plotly_chart(fig_category, use_container_width=True)
            
            # ==================== 4. SCATTER PLOT - STOCK LEVEL vs RETURN RATE ====================
            st.markdown("---")
            st.subheader("🔍 Correlation: Stock Level vs Return Rate")
            
            # Filter out extreme outliers for better visualization
            scatter_df = analysis_df[(analysis_df['stock'] < 500)].copy()
            
            fig_scatter = px.scatter(
                scatter_df,
                x='stock',
                y='return_rate',
                title='Stock Level vs Return Rate Correlation',
                labels={'stock': 'Stock Level', 'return_rate': 'Return Rate (%)'},
                color='return_rate',
                color_continuous_scale='Viridis',
                hover_data=['sku', 'category', 'total_orders'],
                opacity=0.6
            )
            
            # Add trend line
            from scipy import stats
            if len(scatter_df) > 1:
                slope, intercept, r_value, p_value, std_err = stats.linregress(scatter_df['stock'], scatter_df['return_rate'])
                trend_line = slope * scatter_df['stock'] + intercept
                
                import plotly.graph_objects as go
                fig_scatter.add_trace(go.Scatter(
                    x=scatter_df['stock'],
                    y=trend_line,
                    mode='lines',
                    name=f'Trend Line (R²={r_value**2:.3f})',
                    line=dict(color='red', dash='dash')
                ))
            
            fig_scatter.update_layout(height=500)
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Display correlation coefficient
            if len(scatter_df) > 1:
                correlation = scatter_df[['stock', 'return_rate']].corr().iloc[0, 1]
                if abs(correlation) < 0.3:
                    corr_interpretation = "Weak"
                elif abs(correlation) < 0.7:
                    corr_interpretation = "Moderate"
                else:
                    corr_interpretation = "Strong"
                
                st.info(f"📊 Correlation Coefficient: **{correlation:.3f}** ({corr_interpretation} {'positive' if correlation > 0 else 'negative'} correlation)")
            
            # ==================== 5. LINE CHART - RETURN RATE TREND BY MONTH ====================
            st.markdown("---")
            st.subheader("📅 Return Rate Trend Over Time")
            
            # Calculate monthly return rates
            monthly_data = amazon_df.groupby('Month').agg({
                'Order_ID': 'count',
                'is_return': 'sum'
            }).reset_index()
            monthly_data.columns = ['Month', 'total_orders', 'total_returns']
            monthly_data['return_rate'] = (monthly_data['total_returns'] / monthly_data['total_orders']) * 100
            
            # Sort by month
            monthly_data = monthly_data.sort_values('Month')
            
            fig_trend = px.line(
                monthly_data,
                x='Month',
                y='return_rate',
                title='Monthly Return Rate Trend',
                labels={'Month': 'Month', 'return_rate': 'Return Rate (%)'},
                markers=True
            )
            
            fig_trend.update_traces(line_color='#FF6B6B', marker=dict(size=10, color='#FF6B6B'))
            fig_trend.update_layout(
                height=500,
                hovermode='x unified',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
            # Show monthly data table
            with st.expander("📋 View Monthly Return Data"):
                st.dataframe(monthly_data.round(2), use_container_width=True)
            
            # ==================== ADDITIONAL INSIGHTS ====================
            st.markdown("---")
            st.subheader("💡 Key Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🔴 Top 5 Categories with Highest Return Rate")
                top_categories = category_return.head(5)
                for idx, row in top_categories.iterrows():
                    st.write(f"**{row['category']}**: {row['return_rate']:.2f}%")
            
            with col2:
                st.markdown("### 🟢 Top 5 Categories with Lowest Return Rate")
                bottom_categories = category_return.tail(5).sort_values('return_rate')
                for idx, row in bottom_categories.iterrows():
                    st.write(f"**{row['category']}**: {row['return_rate']:.2f}%")
            
        except Exception as e:
            st.error(f"Error in Product Return Analysis: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
    with tab5:
        st.header("📊 Stock & Return Correlation Analysis")
        
        try:
            # Load required data files
            amazon_df = pd.read_csv("new_amazon_national_sales.csv")
            stock_df = pd.read_csv("new_stock_report.csv")
            
            # Clean column names
            amazon_df.columns = amazon_df.columns.str.strip()
            stock_df.columns = stock_df.columns.str.strip()
            
            # ==================== DATA PREPARATION ====================
            
            # Calculate return metrics from Amazon data
            amazon_df['is_return'] = amazon_df['Order_Status'].str.lower().str.contains('cancelled|returned', na=False)
            
            sku_metrics = amazon_df.groupby('sku').agg({
                'Order_ID': 'count',
                'is_return': 'sum',
                'sale': 'mean'  # Average sale price
            }).reset_index()
            sku_metrics.columns = ['sku', 'total_orders', 'total_returns', 'avg_sale_price']
            sku_metrics['return_rate'] = (sku_metrics['total_returns'] / sku_metrics['total_orders']) * 100
            sku_metrics['return_rate'] = sku_metrics['return_rate'].fillna(0)
            
            # Merge stock with return metrics
            merged_df = stock_df.merge(sku_metrics, on='sku', how='left')
            
            # Calculate estimated per-day cost (warehouse cost estimate)
            # Using 0.15 per unit per day as base warehouse cost (from comparison chart)
            merged_df['per-day_cost'] = merged_df['stock'] * 0.15
            
            # For products with sales data, add a small percentage of sale price as holding cost
            merged_df['per-day_cost'] = merged_df['per-day_cost'] + (merged_df['avg_sale_price'].fillna(0) * 0.001)
            
            # Clean and prepare final dataset
            merged_df = merged_df.dropna(subset=['stock', 'category'])
            merged_df['return_rate'] = merged_df['return_rate'].fillna(0)
            merged_df['total_orders'] = merged_df['total_orders'].fillna(0)
            merged_df['per-day_cost'] = merged_df['per-day_cost'].fillna(merged_df['stock'] * 0.15)
            
            # Rename columns for consistency
            merged_df = merged_df.rename(columns={
                'stock': 'Stock_Level',
                'category': 'Product_Category',
                'sku': 'Product_SKU'
            })
            
            # ==================== KEY METRICS ====================
            st.subheader("📈 Overview Metrics")
            
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                avg_return_rate = merged_df['return_rate'].mean()
                st.metric("Avg Return Rate", f"{avg_return_rate:.2f}%")
            
            with metric_col2:
                total_stock = merged_df['Stock_Level'].sum()
                st.metric("Total Stock Units", f"{total_stock:,.0f}")
            
            with metric_col3:
                avg_cost = merged_df['per-day_cost'].mean()
                st.metric("Avg Cost/Day", f"₹{avg_cost:.2f}")
            
            with metric_col4:
                high_risk_count = len(merged_df[(merged_df['return_rate'] > 70) & 
                                               (merged_df['Stock_Level'] > merged_df['Stock_Level'].median())])
                st.metric("High-Risk Products", high_risk_count)
            
            # ==================== SCATTER PLOT 1: STOCK vs RETURN RATE ====================
            st.markdown("---")
            st.subheader("🔵 Stock Level vs Return Rate Analysis")
            
            # Filter for better visualization (remove extreme outliers)
            scatter_df1 = merged_df[merged_df['Stock_Level'] < 500].copy()
            
            fig_scatter1 = px.scatter(
                scatter_df1,
                x='Stock_Level',
                y='return_rate',
                size='per-day_cost',
                color='Product_Category',
                hover_name='Product_SKU',
                hover_data={
                    'Stock_Level': True,
                    'return_rate': ':.2f',
                    'per-day_cost': ':.2f',
                    'total_orders': True
                },
                title='Stock Level vs Return Rate (Bubble size = Cost per day)',
                labels={
                    'Stock_Level': 'Stock Level',
                    'return_rate': 'Return Rate (%)',
                    'per-day_cost': 'Per-day Cost (₹)'
                },
                size_max=30
            )
            
            fig_scatter1.update_layout(height=600)
            st.plotly_chart(fig_scatter1, use_container_width=True)
            
            # Conclusion for Scatter Plot 1
            stock_return_corr_1 = scatter_df1[['Stock_Level', 'return_rate']].corr().iloc[0, 1]
            high_stock_high_return = scatter_df1[(scatter_df1['Stock_Level'] > scatter_df1['Stock_Level'].quantile(0.75)) & 
                                                  (scatter_df1['return_rate'] > 50)]
            
            st.markdown("### 📝 Conclusion:")
            if stock_return_corr_1 > 0.3:
                st.warning(f"""
                **⚠️ Concerning Pattern Detected**  
                - Products with higher stock levels tend to have higher return rates (correlation: {stock_return_corr_1:.3f})
                - **{len(high_stock_high_return)} products** have both high stock (top 25%) and high return rates (>50%)
                - **Implication**: You may be overstocking products that customers don't like or have quality issues
                - **Action**: Review high-stock, high-return items for quality, description accuracy, or discontinuation
                """)
            elif stock_return_corr_1 < -0.3:
                st.success(f"""
                **✅ Positive Pattern**  
                - Products with higher stock levels have LOWER return rates (correlation: {stock_return_corr_1:.3f})
                - **Implication**: You're stocking more of the products customers love and keep
                - **Action**: Continue this strategy - stock up on winners!
                """)
            else:
                st.info(f"""
                **ℹ️ No Strong Relationship**  
                - Stock levels and return rates are largely independent (correlation: {stock_return_corr_1:.3f})
                - **Implication**: How much you stock doesn't affect return likelihood
                - **Action**: Returns are driven by other factors (quality, fit, description) - focus inventory decisions on demand forecasting
                """)
            
            # ==================== SCATTER PLOT 2: COST vs RETURN RATE ====================
            st.markdown("---")
            st.subheader(" Per-day Cost vs Return Rate Analysis")
            
            # Filter for better visualization
            scatter_df2 = merged_df[merged_df['per-day_cost'] < 100].copy()
            
            fig_scatter2 = px.scatter(
                scatter_df2,
                x='per-day_cost',
                y='return_rate',
                size='Stock_Level',
                color='Product_Category',
                hover_name='Product_SKU',
                hover_data={
                    'per-day_cost': ':.2f',
                    'return_rate': ':.2f',
                    'Stock_Level': True,
                    'total_orders': True
                },
                title='Per-day Cost vs Return Rate (Bubble size = Stock Level)',
                labels={
                    'per-day_cost': 'Per-day Cost (₹)',
                    'return_rate': 'Return Rate (%)',
                    'Stock_Level': 'Stock Level'
                },
                size_max=30
            )
            
            fig_scatter2.update_layout(height=600)
            st.plotly_chart(fig_scatter2, use_container_width=True)
            
            # Conclusion for Scatter Plot 2
            cost_return_corr = scatter_df2[['per-day_cost', 'return_rate']].corr().iloc[0, 1]
            high_cost_high_return = scatter_df2[(scatter_df2['per-day_cost'] > scatter_df2['per-day_cost'].quantile(0.75)) & 
                                                (scatter_df2['return_rate'] > 50)]
            total_waste_cost = high_cost_high_return['per-day_cost'].sum()
            
            st.markdown("### 📝 Conclusion:")
            if len(high_cost_high_return) > 0:
                st.error(f"""
                **💸 High Financial Risk Identified**  
                - **{len(high_cost_high_return)} products** have both high daily costs (top 25%) and high return rates (>50%)
                - **Daily cost impact**: ₹{total_waste_cost:,.2f} spent holding frequently-returned items
                - **Correlation**: {cost_return_corr:.3f} - {'Strong' if abs(cost_return_corr) > 0.7 else 'Moderate' if abs(cost_return_corr) > 0.3 else 'Weak'} relationship
                - **Action**: Prioritize investigating expensive-to-hold items with high returns - these hurt profitability most
                """)
            else:
                st.success(f"""
                **✅ Good Cost Management**  
                - No products with both high costs and high return rates
                - **Correlation**: {cost_return_corr:.3f} - expensive items aren't being returned excessively
                - **Action**: Continue monitoring, but current cost-return balance is healthy
                """)
            
            # ==================== BAR CHART: AVERAGE RETURN RATE BY CATEGORY ====================
            st.markdown("---")
            st.subheader("📊 Average Return Rate by Product Category")
            
            category_avg = merged_df.groupby('Product_Category')['return_rate'].mean().reset_index()
            category_avg = category_avg.sort_values('return_rate', ascending=False)
            
            fig_category = px.bar(
                category_avg,
                x='Product_Category',
                y='return_rate',
                title='Average Return Rate by Category',
                labels={
                    'Product_Category': 'Product Category',
                    'return_rate': 'Average Return Rate (%)'
                },
                color='return_rate',
                color_continuous_scale='Reds'
            )
            
            fig_category.update_layout(
                xaxis_tickangle=-45,
                height=500,
                showlegend=False
            )
            st.plotly_chart(fig_category, use_container_width=True)
            
            # Conclusion for Bar Chart
            worst_category = category_avg.iloc[0]
            best_category = category_avg.iloc[-1]
            avg_overall = category_avg['return_rate'].mean()
            high_return_categories = category_avg[category_avg['return_rate'] > 50]
            
            st.markdown("### 📝 Conclusion:")
            if len(high_return_categories) > 0:
                st.warning(f"""
                **⚠️ Problem Categories Identified**  
                - **Worst performer**: {worst_category['Product_Category']} ({worst_category['return_rate']:.1f}% return rate)
                - **Best performer**: {best_category['Product_Category']} ({best_category['return_rate']:.1f}% return rate)
                - **{len(high_return_categories)} categories** have >50% return rates
                - **Overall average**: {avg_overall:.1f}%
                - **Action**: Focus quality control and customer feedback analysis on high-return categories
                - **Consider**: Category-specific improvements (sizing guides, better photos, material descriptions)
                """)
            else:
                st.success(f"""
                **✅ Good Category Performance**  
                - **Worst performer**: {worst_category['Product_Category']} ({worst_category['return_rate']:.1f}% return rate)
                - **Best performer**: {best_category['Product_Category']} ({best_category['return_rate']:.1f}% return rate)
                - All categories have <50% return rates
                - **Overall average**: {avg_overall:.1f}%
                - **Action**: Maintain current quality standards while optimizing worst-performing category
                """)
            
            # ==================== HIGH-RISK TABLE ====================
            st.markdown("---")
            st.subheader("🚨 High-Risk Overstocked Products (High Cost & Return)")
            
            # Calculate median stock level
            median_stock = merged_df['Stock_Level'].median()
            
            # Filter high-risk products
            high_risk_df = merged_df[
                (merged_df['return_rate'] > 70) & 
                (merged_df['Stock_Level'] > median_stock)
            ].copy()
            
            if len(high_risk_df) > 0:
                # Sort by return rate and cost
                high_risk_df = high_risk_df.sort_values(['return_rate', 'per-day_cost'], ascending=[False, False])
                
                # Display the table
                st.warning(f"⚠️ Found **{len(high_risk_df)} high-risk products** with >70% return rate and above-median stock levels")
                
                display_df = high_risk_df[[
                    'Product_SKU', 
                    'Product_Category', 
                    'Stock_Level', 
                    'per-day_cost', 
                    'return_rate', 
                    'total_orders'
                ]].copy()
                
                # Format columns
                display_df['per-day_cost'] = display_df['per-day_cost'].round(2)
                display_df['return_rate'] = display_df['return_rate'].round(2)
                display_df['Stock_Level'] = display_df['Stock_Level'].astype(int)
                display_df['total_orders'] = display_df['total_orders'].astype(int)
                
                st.dataframe(display_df, use_container_width=True)
                
                # Calculate financial impact
                total_cost_impact = (high_risk_df['per-day_cost']).sum()
                monthly_impact = total_cost_impact * 30
                st.error(f"💸 **Daily Holding Cost for High-Risk Items**: ₹{total_cost_impact:,.2f} | **Monthly**: ₹{monthly_impact:,.2f}")
                
                # Recommendations
                st.markdown("### 💡 Recommended Actions:")
                st.markdown("""
                - 🔴 **Immediate**: Stop restocking these items
                - 📉 **Short-term**: Offer discounts to clear inventory
                - 🔍 **Investigation**: Analyze why return rates are high (quality, sizing, description)
                - 📊 **Long-term**: Consider discontinuing poor performers
                """)
                
                # Conclusion for High-Risk Table
                st.markdown("### 📝 Conclusion:")
                st.error(f"""
                **🚨 Critical Action Required**  
                - You're spending ₹{total_cost_impact:,.2f}/day (₹{monthly_impact:,.2f}/month) to hold {len(high_risk_df)} products that customers frequently return
                - These products have >70% return rates AND higher-than-median inventory levels
                - **Financial waste**: Every day these items sit in the warehouse costs money while generating returns
                - **Urgency**: High priority - address within 30 days to minimize losses
                - **Next steps**: Review top 5 items immediately, investigate root causes, implement corrective actions
                """)
            else:
                st.success("✅ No high-risk overstocked products found!")
            
            # ==================== CORRELATION ANALYSIS ====================
            st.markdown("---")
            st.subheader("📈 Correlation Matrix")
            
            # Calculate correlations
            corr_df = merged_df[['Stock_Level', 'per-day_cost', 'return_rate', 'total_orders']].corr()
            
            # Create heatmap
            fig_corr = px.imshow(
                corr_df,
                text_auto='.3f',
                aspect='auto',
                color_continuous_scale='RdBu_r',
                title='Correlation Heatmap: Stock, Cost, Returns, Orders',
                labels=dict(color="Correlation")
            )
            
            fig_corr.update_layout(height=500)
            st.plotly_chart(fig_corr, use_container_width=True)
            
            # Interpretation
            stock_return_corr = corr_df.loc['Stock_Level', 'return_rate']
            cost_return_corr = corr_df.loc['per-day_cost', 'return_rate']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(f"""
                **Stock Level ↔ Return Rate**  
                Correlation: **{stock_return_corr:.3f}**  
                {
                    'Strong positive - More stock = More returns ⚠️' if stock_return_corr > 0.7 else
                    'Moderate positive - Some correlation' if stock_return_corr > 0.3 else
                    'Weak - Little to no relationship ✓' if abs(stock_return_corr) < 0.3 else
                    'Negative - More stock = Fewer returns ✓'
                }
                """)
            
            with col2:
                st.info(f"""
                **Per-day Cost ↔ Return Rate**  
                Correlation: **{cost_return_corr:.3f}**  
                {
                    'Strong positive - Higher cost = More returns ⚠️' if cost_return_corr > 0.7 else
                    'Moderate positive - Some correlation' if cost_return_corr > 0.3 else
                    'Weak - Little to no relationship ✓' if abs(cost_return_corr) < 0.3 else
                    'Negative - Higher cost = Fewer returns ✓'
                }
                """)
            
            # Overall Conclusion for Correlation Matrix
            st.markdown("---")
            st.markdown("### 📝 Overall Correlation Analysis:")
            
            orders_return_corr = corr_df.loc['total_orders', 'return_rate']
            stock_cost_corr = corr_df.loc['Stock_Level', 'per-day_cost']
            
            st.success(f"""
            **🎯 Key Findings:**
            
            **Inventory Management:**
            - Stock ↔ Returns: {stock_return_corr:.3f} → {'Your stock levels ARE affecting returns' if abs(stock_return_corr) > 0.3 else 'Stock levels don\'t drive returns'}
            - Stock ↔ Cost: {stock_cost_corr:.3f} → {'Expected positive relationship - more stock = higher costs' if stock_cost_corr > 0.5 else 'Costs vary independently of stock'}
            
            **Product Performance:**
            - Orders ↔ Returns: {orders_return_corr:.3f} → {'Popular items have high returns' if orders_return_corr > 0.3 else 'Popular items aren\'t necessarily returned more' if abs(orders_return_corr) < 0.3 else 'Popular items have fewer returns'}
            - Cost ↔ Returns: {cost_return_corr:.3f} → {'Expensive items cause returns' if cost_return_corr > 0.3 else 'Cost doesn\'t affect return likelihood'}
            
            **Strategic Recommendation:**
            {
                '⚠️ CRITICAL: Your inventory decisions directly impact returns. Focus on stocking low-return products.' if abs(stock_return_corr) > 0.5 else
                '✅ GOOD: Returns are driven by product quality/fit, not how much you stock. Focus on product improvements rather than inventory adjustments.'
            }
            """)
            
        except Exception as e:
            st.error(f"Error in Stock & Return Correlation Analysis: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
    with tab6:
        st.header("👥 Customer Insights")
        
        try:
            # Load data
            customers_df = pd.read_csv("new_international_sales_report.csv")
            
            # Clean column names
            customers_df.columns = customers_df.columns.str.strip()
            
            # Convert date to datetime
            customers_df['date'] = pd.to_datetime(customers_df['date'], format='%d-%m-%Y', errors='coerce')
            
            # Convert numeric columns safely
            customers_df['Gross_Amount'] = pd.to_numeric(customers_df['Gross_Amount'], errors='coerce')
            customers_df['Quantity_Purchased'] = pd.to_numeric(customers_df['Quantity_Purchased'], errors='coerce')
            
            # Drop rows with missing critical data
            customers_df = customers_df.dropna(subset=['Customer_Name', 'Gross_Amount', 'date'])
            
            # ==================== 1. TOP CUSTOMERS BY SALES ====================
            st.subheader("🏆 Top 10 Customers by Sales")
            
            # Group by customer and sum gross amount
            top_customers = customers_df.groupby('Customer_Name')['Gross_Amount'].sum().reset_index()
            top_customers = top_customers.sort_values('Gross_Amount', ascending=False).head(10)
            
            # Create bar chart
            fig_top_customers = px.bar(
                top_customers,
                x='Customer_Name',
                y='Gross_Amount',
                title='Top 10 Customers by Total Purchase',
                labels={'Customer_Name': 'Customer', 'Gross_Amount': 'Total Purchase (₹)'},
                color='Gross_Amount',
                color_continuous_scale='Blues'
            )
            
            fig_top_customers.update_layout(
                xaxis_tickangle=-45,
                height=500,
                yaxis=dict(tickformat=','),
                showlegend=False
            )
            
            st.plotly_chart(fig_top_customers, use_container_width=True)
            
            # Show summary metrics for top customers
            col1, col2, col3 = st.columns(3)
            with col1:
                top_customer_name = top_customers.iloc[0]['Customer_Name']
                top_customer_value = top_customers.iloc[0]['Gross_Amount']
                st.metric("Top Customer", top_customer_name, f"₹{top_customer_value:,.0f}")
            
            with col2:
                top_10_total = top_customers['Gross_Amount'].sum()
                st.metric("Top 10 Total Sales", f"₹{top_10_total:,.0f}")
            
            with col3:
                overall_total = customers_df['Gross_Amount'].sum()
                top_10_percent = (top_10_total / overall_total) * 100
                st.metric("Top 10 Share", f"{top_10_percent:.1f}%")
            
            # ==================== 2. CUSTOMER PURCHASE PATTERNS ====================
            st.markdown("---")
            st.subheader("🔍 Customer Purchase Patterns")
            
            # New Customer Acquisition by Month - Show always
            st.markdown("### 📈 New Customer Acquisition Trend")
            
            # Get first purchase date for each customer
            first_purchase = customers_df.groupby('Customer_Name')['date'].min().reset_index()
            first_purchase.columns = ['Customer_Name', 'First_Purchase_Date']
            
            # Extract month and count new customers per month
            first_purchase['Month'] = first_purchase['First_Purchase_Date'].dt.to_period('M').astype(str)
            monthly_new_customers = first_purchase.groupby('Month').size().reset_index(name='New_Customers')
            monthly_new_customers = monthly_new_customers.sort_values('Month')
            
            # Create line chart
            fig_acquisition = px.line(
                monthly_new_customers,
                x='Month',
                y='New_Customers',
                title='New Customer Acquisition by Month',
                labels={'Month': 'Month', 'New_Customers': 'New Customers'},
                markers=True
            )
            
            fig_acquisition.update_traces(line_color='#1f77b4', marker=dict(size=8))
            fig_acquisition.update_layout(
                height=500,
                xaxis_tickangle=-45,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_acquisition, use_container_width=True)
            
            # Create customer selector with default value
            st.markdown("---")
            st.markdown("### 👤 Individual Customer Analysis")
            
            customer_list = ['All'] + sorted(customers_df['Customer_Name'].unique().tolist())
            
            # Set default to customer containing "avin" (case-insensitive), otherwise first customer
            default_customer = 'All'
            for customer in customer_list:
                if customer.lower() == 'avin' or 'avin' in customer.lower():
                    default_customer = customer
                    break
            
            # If no avin found, use first actual customer (not "All")
            if default_customer == 'All' and len(customer_list) > 1:
                default_customer = customer_list[1]
            
            default_index = customer_list.index(default_customer)
            
            selected_customer = st.selectbox("Select Customer", customer_list, index=default_index)
            
            if selected_customer == 'All':
                # Show overall metrics
                st.markdown("### 📊 Overall Customer Metrics")
                
                metric_col1, metric_col2 = st.columns(2)
                
                with metric_col1:
                    total_customers = customers_df['Customer_Name'].nunique()
                    st.metric("Total Customers", f"{total_customers:,}")
                
                with metric_col2:
                    avg_customer_spend = customers_df.groupby('Customer_Name')['Gross_Amount'].sum().mean()
                    st.metric("Average Customer Spend", f"₹{avg_customer_spend:,.2f}")
                
                # Additional insights
                st.markdown("---")
                st.markdown("### 💡 Key Insights")
                
                # Customer concentration analysis
                customer_sales = customers_df.groupby('Customer_Name')['Gross_Amount'].sum().sort_values(ascending=False)
                top_20_percent_customers = int(len(customer_sales) * 0.2)
                top_20_sales = customer_sales.head(top_20_percent_customers).sum()
                top_20_contribution = (top_20_sales / customer_sales.sum()) * 100
                
                insight_col1, insight_col2 = st.columns(2)
                
                with insight_col1:
                    st.info(f"""
                    **📊 Customer Concentration (80/20 Rule)**  
                    - Top 20% of customers ({top_20_percent_customers} customers)
                    - Contribute **{top_20_contribution:.1f}%** of total sales
                    - {'⚠️ High concentration risk' if top_20_contribution > 80 else '✅ Balanced customer base'}
                    """)
                
                with insight_col2:
                    # Repeat vs one-time customers
                    purchase_counts = customers_df.groupby('Customer_Name').size()
                    repeat_customers = (purchase_counts > 1).sum()
                    repeat_rate = (repeat_customers / total_customers) * 100
                    
                    st.success(f"""
                    **🔄 Customer Loyalty**  
                    - **{repeat_customers:,}** repeat customers ({repeat_rate:.1f}%)
                    - **{total_customers - repeat_customers:,}** one-time customers
                    - {'✅ Strong retention' if repeat_rate > 50 else '⚠️ Focus on retention strategies'}
                    """)
            
            else:
                # Show specific customer analysis
                customer_data = customers_df[customers_df['Customer_Name'] == selected_customer].copy()
                
                if len(customer_data) > 0:
                    st.markdown(f"### 📋 Profile: {selected_customer}")
                    
                    # Customer summary metrics
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
                    with metric_col1:
                        total_purchases = customer_data['Gross_Amount'].sum()
                        st.metric("Total Spent", f"₹{total_purchases:,.0f}")
                    
                    with metric_col2:
                        total_orders = len(customer_data)
                        st.metric("Total Orders", total_orders)
                    
                    with metric_col3:
                        avg_order_value = customer_data['Gross_Amount'].mean()
                        st.metric("Avg Order Value", f"₹{avg_order_value:,.0f}")
                    
                    with metric_col4:
                        total_items = customer_data['Quantity_Purchased'].sum()
                        st.metric("Total Items Purchased", int(total_items))
                    
                    # Two side-by-side charts
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Bar chart: Purchase history over time
                        st.markdown("#### 📅 Purchase History")
                        
                        # Extract month-year from date and aggregate
                        customer_data_copy = customer_data.copy()
                        customer_data_copy['Month_Year'] = customer_data_copy['date'].dt.strftime('%b-%Y')
                        customer_data_copy['Month_Sort'] = customer_data_copy['date'].dt.to_period('M')
                        
                        # Group by month-year
                        purchase_history = customer_data_copy.groupby(['Month_Year', 'Month_Sort']).agg({
                            'Gross_Amount': 'sum',
                            'Quantity_Purchased': 'sum'
                        }).reset_index()
                        purchase_history = purchase_history.sort_values('Month_Sort')
                        purchase_history['Order_Count'] = customer_data_copy.groupby(['Month_Year', 'Month_Sort']).size().values
                        
                        # Check if customer has purchases across multiple months
                        unique_months = len(purchase_history)
                        
                        if unique_months == 1:
                            # Show message if all purchases in one month
                            st.info(f"ℹ️ All {len(customer_data)} orders were placed in {purchase_history.iloc[0]['Month_Year']}")
                        
                        # Create line chart with month on x-axis
                        fig_history = px.line(
                            purchase_history,
                            x='Month_Year',
                            y='Gross_Amount',
                            title=f'Monthly Purchase History ({unique_months} month{"s" if unique_months > 1 else ""}, {len(customer_data)} orders)',
                            labels={'Month_Year': 'Month', 'Gross_Amount': 'Amount (₹)'},
                            hover_data={'Quantity_Purchased': True, 'Order_Count': True},
                            markers=True
                        )
                        
                        fig_history.update_traces(
                            line_color='#2ecc71',
                            marker=dict(size=10, color='#2ecc71'),
                            hovertemplate='<b>Month:</b> %{x}<br><b>Amount:</b> ₹%{y:,.0f}<br><b>Items:</b> %{customdata[0]}<br><b>Orders:</b> %{customdata[1]}<extra></extra>'
                        )
                        fig_history.update_layout(
                            height=400,
                            yaxis=dict(tickformat=','),
                            xaxis=dict(tickangle=-45),
                            hovermode='closest',
                            showlegend=False
                        )
                        
                        st.plotly_chart(fig_history, use_container_width=True)
                    
                    with col2:
                        # Pie chart: Product preferences by style
                        st.markdown("#### 👗 Product Preferences")
                        
                        style_preferences = customer_data.groupby('style')['Gross_Amount'].sum().reset_index()
                        style_preferences = style_preferences.sort_values('Gross_Amount', ascending=False)
                        
                        fig_preferences = px.pie(
                            style_preferences,
                            values='Gross_Amount',
                            names='style',
                            title='Spending by Product Style',
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        
                        fig_preferences.update_traces(textposition='inside', textinfo='percent+label')
                        fig_preferences.update_layout(height=400)
                        
                        st.plotly_chart(fig_preferences, use_container_width=True)
                    
                    # Customer insights
                    st.markdown("### 💡 Customer Insights")
                    
                    first_purchase = customer_data['date'].min()
                    last_purchase = customer_data['date'].max()
                    customer_lifetime = (last_purchase - first_purchase).days
                    
                    favorite_style = style_preferences.iloc[0]['style']
                    favorite_style_spend = style_preferences.iloc[0]['Gross_Amount']
                    favorite_style_percent = (favorite_style_spend / total_purchases) * 100
                    
                    st.info(f"""
                    **📊 Customer Behavior Analysis:**
                    - **Customer Since**: {first_purchase.strftime('%B %d, %Y')}
                    - **Last Purchase**: {last_purchase.strftime('%B %d, %Y')}
                    - **Customer Lifetime**: {customer_lifetime} days
                    - **Favorite Style**: {favorite_style} ({favorite_style_percent:.1f}% of spending)
                    - **Average Order Value**: ₹{avg_order_value:,.0f}
                    - **Purchase Frequency**: {total_orders / max(1, customer_lifetime / 30):.1f} orders per month
                    """)
                else:
                    st.warning("No data found for this customer.")
            
        except Exception as e:
            st.error(f"Error in Customer Insights: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
    with tab7:
        st.header("💰 Product Profit Margin Analysis")
        
        try:
            import plotly.graph_objects as go
            import numpy as np
            
            # Year selection with radio button
            st.subheader("📅 Select Year for Analysis")
            selected_year = st.radio(
                "Choose Year",
                options=["March 2021", "May 2022"],
                horizontal=True
            )
            
            # Determine file and cost column based on year
            if selected_year == "March 2021":
                file_name = "new_2021_product_info.csv"
                year_label = "2021"
            else:
                file_name = "new_2022_product_info.csv"
                year_label = "2022"
            
            try:
                # Load dataset
                df_year = pd.read_csv(file_name)
                
                # Clean column names
                df_year.columns = df_year.columns.str.strip()
                
                # Verify required columns exist
                required_cols = ['sku', 'cost_price', 'mrp']
                missing_cols = [col for col in required_cols if col not in df_year.columns]
                
                if missing_cols:
                    st.error(f"❌ Missing required columns: {missing_cols}")
                    st.info(f"Available columns: {list(df_year.columns)}")
                else:
                    # Convert to numeric
                    df_year['cost_price'] = pd.to_numeric(df_year['cost_price'], errors='coerce')
                    df_year['mrp'] = pd.to_numeric(df_year['mrp'], errors='coerce')
                    
                    # Remove rows with NaN values
                    df_year = df_year.dropna(subset=['cost_price', 'mrp'])
                    
                    # Calculate Profit Amount and Profit Margin %
                    df_year['Profit_Amount'] = df_year['mrp'] - df_year['cost_price']
                    df_year['Profit_Margin_%'] = ((df_year['mrp'] - df_year['cost_price']) / df_year['cost_price']) * 100
                    
                    # Handle infinite values
                    df_year = df_year.replace([np.inf, -np.inf], np.nan)
                    df_year = df_year.dropna(subset=['Profit_Margin_%'])
                    
                    # ==================== KEY METRICS ====================
                    st.markdown("---")
                    st.subheader(f"📊 Summary Metrics for {selected_year}")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        avg_margin = df_year['Profit_Margin_%'].mean()
                        st.metric("Average Profit Margin", f"{avg_margin:.2f}%")
                    
                    with col2:
                        median_margin = df_year['Profit_Margin_%'].median()
                        st.metric("Median Profit Margin", f"{median_margin:.2f}%")
                    
                    with col3:
                        total_products = len(df_year)
                        st.metric("Total Products Analyzed", f"{total_products:,}")
                    
                    # ==================== FILTERS ====================
                    st.markdown("---")
                    st.subheader("🔍 Filters")
                    
                    filter_col1, filter_col2 = st.columns(2)
                    
                    with filter_col1:
                        # Category filter
                        if 'category' in df_year.columns:
                            all_categories = ['All'] + sorted(df_year['category'].dropna().unique().tolist())
                            selected_category = st.selectbox("Select Product Category", all_categories)
                        else:
                            selected_category = 'All'
                            st.info("No category column found in dataset")
                    
                    with filter_col2:
                        # Profit Margin Range slider
                        min_margin = float(df_year['Profit_Margin_%'].min())
                        max_margin = float(df_year['Profit_Margin_%'].max())
                        
                        margin_range = st.slider(
                            "Select Profit Margin Range (%)",
                            min_value=min_margin,
                            max_value=max_margin,
                            value=(min_margin, max_margin),
                            step=0.1
                        )
                    
                    # Apply filters
                    df_filtered = df_year.copy()
                    
                    if selected_category != 'All' and 'category' in df_year.columns:
                        df_filtered = df_filtered[df_filtered['category'] == selected_category]
                    
                    df_filtered = df_filtered[
                        (df_filtered['Profit_Margin_%'] >= margin_range[0]) & 
                        (df_filtered['Profit_Margin_%'] <= margin_range[1])
                    ]
                    
                    # ==================== FILTERED DATA TABLE ====================
                    st.markdown("---")
                    st.subheader(f"📋 Product Profit Margins ({len(df_filtered)} products)")
                    
                    if len(df_filtered) > 0:
                        # Prepare display dataframe
                        display_cols = ['sku', 'cost_price', 'mrp', 'Profit_Amount', 'Profit_Margin_%']
                        
                        # Add optional columns if they exist
                        if 'category' in df_filtered.columns:
                            display_cols.append('category')
                        if 'catalog' in df_filtered.columns:
                            display_cols.append('catalog')
                        
                        display_df = df_filtered[display_cols].copy()
                        
                        # Rename columns
                        column_names = {
                            'sku': 'Product SKU',
                            'cost_price': 'Transfer Price (₹)',
                            'mrp': 'MRP (₹)',
                            'Profit_Amount': 'Profit Amount (₹)',
                            'Profit_Margin_%': 'Profit Margin (%)',
                            'category': 'Category',
                            'catalog': 'Catalog'
                        }
                        display_df = display_df.rename(columns=column_names)
                        
                        # Format numeric columns
                        for col in ['Transfer Price (₹)', 'MRP (₹)', 'Profit Amount (₹)']:
                            if col in display_df.columns:
                                display_df[col] = display_df[col].round(2)
                        
                        if 'Profit Margin (%)' in display_df.columns:
                            display_df['Profit Margin (%)'] = display_df['Profit Margin (%)'].round(2)
                        
                        st.dataframe(display_df, use_container_width=True, height=400)
                    else:
                        st.warning("⚠️ No products match the selected filters.")
                    
                    # ==================== VISUALIZATIONS ====================
                    if len(df_filtered) > 0:
                        st.markdown("---")
                        st.subheader("📈 Profit Margin Visualizations")
                        
                        # 1. HISTOGRAM: Profit Margin Distribution
                        st.markdown("### 📊 Profit Margin Distribution")
                        
                        fig_hist = px.histogram(
                            df_filtered,
                            x='Profit_Margin_%',
                            nbins=30,
                            title=f'Profit Margin Distribution - {selected_year}',
                            labels={'Profit_Margin_%': 'Profit Margin (%)'},
                            color_discrete_sequence=['#3498db']
                        )
                        
                        # Add mean line
                        mean_margin = df_filtered['Profit_Margin_%'].mean()
                        fig_hist.add_vline(
                            x=mean_margin,
                            line_dash="dash",
                            line_color="red",
                            annotation_text=f"Mean: {mean_margin:.2f}%",
                            annotation_position="top right"
                        )
                        
                        fig_hist.update_layout(
                            xaxis_title="Profit Margin (%)",
                            yaxis_title="Number of Products",
                            showlegend=False,
                            height=400,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            margin=dict(l=50, r=50, t=50, b=50)
                        )
                        
                        st.plotly_chart(fig_hist, use_container_width=True)
                        
                        # 2. SCATTER PLOT: Cost Price vs MRP
                        st.markdown("---")
                        st.markdown("### 📍 Transfer Price vs MRP Scatter Plot")
                        
                        fig_scatter = px.scatter(
                            df_filtered,
                            x='cost_price',
                            y='mrp',
                            color='Profit_Margin_%',
                            hover_data=['sku'],
                            title=f'Transfer Price vs MRP - {selected_year}',
                            labels={
                                'cost_price': 'Transfer Price (₹)',
                                'mrp': 'MRP (₹)',
                                'Profit_Margin_%': 'Profit Margin (%)'
                            },
                            color_continuous_scale='Viridis'
                        )
                        
                        # Add reference line (MRP = Cost)
                        max_val = max(df_filtered['cost_price'].max(), df_filtered['mrp'].max())
                        fig_scatter.add_trace(
                            go.Scatter(
                                x=[0, max_val],
                                y=[0, max_val],
                                mode='lines',
                                name='Equal Price Line',
                                line=dict(color='red', dash='dash', width=2)
                            )
                        )
                        
                        fig_scatter.update_layout(
                            height=400,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            margin=dict(l=50, r=50, t=50, b=50)
                        )
                        st.plotly_chart(fig_scatter, use_container_width=True)
                        
                        # 3. CATEGORY-WISE ANALYSIS
                        if 'category' in df_filtered.columns and len(df_filtered['category'].unique()) > 1:
                            st.markdown("---")
                            st.markdown("### 📦 Category-wise Profit Analysis")
                            
                            # Calculate category statistics
                            category_stats = df_filtered.groupby('category').agg({
                                'Profit_Margin_%': ['mean', 'median', 'min', 'max', 'count']
                            }).round(2)
                            
                            category_stats.columns = ['Average Margin (%)', 'Median Margin (%)', 
                                                     'Min Margin (%)', 'Max Margin (%)', 'Product Count']
                            category_stats = category_stats.reset_index()
                            category_stats = category_stats.sort_values('Average Margin (%)', ascending=False)
                            
                            # Display table
                            st.dataframe(category_stats, use_container_width=True, hide_index=True)
                            
                            # Bar chart
                            st.markdown("#### Average Profit Margin by Category")
                            
                            fig_category = px.bar(
                                category_stats,
                                x='category',
                                y='Average Margin (%)',
                                color='Average Margin (%)',
                                title=f'Average Profit Margin by Category - {selected_year}',
                                labels={'category': 'Product Category'},
                                color_continuous_scale='RdYlGn',
                                text='Average Margin (%)'
                            )
                            
                            fig_category.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                            fig_category.update_layout(
                                xaxis_tickangle=-45,
                                height=400,
                                showlegend=False,
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                margin=dict(l=50, r=50, t=50, b=80)
                            )
                            
                            st.plotly_chart(fig_category, use_container_width=True)
                    
                    # ==================== YEAR-OVER-YEAR COMPARISON ====================
                    st.markdown("---")
                    st.subheader("🔄 Year-over-Year Comparison (March 2021 vs May 2022)")
                    
                    try:
                        # Load both datasets
                        df_2021 = pd.read_csv("new_2021_product_info.csv")
                        df_2022 = pd.read_csv("new_2022_product_info.csv")
                        
                        # Clean column names
                        df_2021.columns = df_2021.columns.str.strip()
                        df_2022.columns = df_2022.columns.str.strip()
                        
                        # Convert to numeric
                        for df_temp in [df_2021, df_2022]:
                            df_temp['cost_price'] = pd.to_numeric(df_temp['cost_price'], errors='coerce')
                            df_temp['mrp'] = pd.to_numeric(df_temp['mrp'], errors='coerce')
                        
                        # Remove NaN
                        df_2021 = df_2021.dropna(subset=['cost_price', 'mrp'])
                        df_2022 = df_2022.dropna(subset=['cost_price', 'mrp'])
                        
                        # Calculate margins
                        df_2021['Profit_Margin_%'] = ((df_2021['mrp'] - df_2021['cost_price']) / df_2021['cost_price']) * 100
                        df_2022['Profit_Margin_%'] = ((df_2022['mrp'] - df_2022['cost_price']) / df_2022['cost_price']) * 100
                        
                        # Handle infinite values
                        df_2021 = df_2021.replace([np.inf, -np.inf], np.nan).dropna(subset=['Profit_Margin_%'])
                        df_2022 = df_2022.replace([np.inf, -np.inf], np.nan).dropna(subset=['Profit_Margin_%'])
                        
                        # Comparison metrics
                        st.markdown("### 📊 Overall Metrics Comparison")
                        
                        comp_col1, comp_col2, comp_col3 = st.columns(3)
                        
                        with comp_col1:
                            avg_2021 = df_2021['Profit_Margin_%'].mean()
                            avg_2022 = df_2022['Profit_Margin_%'].mean()
                            change = avg_2022 - avg_2021
                            st.metric(
                                "Average Margin Change",
                                f"{avg_2022:.2f}%",
                                f"{change:+.2f}%",
                                delta_color="normal" if change > 0 else "inverse"
                            )
                        
                        with comp_col2:
                            med_2021 = df_2021['Profit_Margin_%'].median()
                            med_2022 = df_2022['Profit_Margin_%'].median()
                            med_change = med_2022 - med_2021
                            st.metric(
                                "Median Margin Change",
                                f"{med_2022:.2f}%",
                                f"{med_change:+.2f}%",
                                delta_color="normal" if med_change > 0 else "inverse"
                            )
                        
                        with comp_col3:
                            common_skus = set(df_2021['sku']).intersection(set(df_2022['sku']))
                            st.metric("Common Products", f"{len(common_skus):,}")
                        
                        # Overlay histogram
                        st.markdown("---")
                        st.markdown("### 📊 Profit Margin Distribution Comparison")
                        
                        # Create combined dataframe for overlay
                        df_2021_plot = df_2021[['Profit_Margin_%']].copy()
                        df_2021_plot['Year'] = 'March 2021'
                        
                        df_2022_plot = df_2022[['Profit_Margin_%']].copy()
                        df_2022_plot['Year'] = 'May 2022'
                        
                        df_combined = pd.concat([df_2021_plot, df_2022_plot], ignore_index=True)
                        
                        fig_overlay = px.histogram(
                            df_combined,
                            x='Profit_Margin_%',
                            color='Year',
                            nbins=30,
                            barmode='group',
                            title='Profit Margin Distribution - March 2021 vs May 2022',
                            labels={'Profit_Margin_%': 'Profit Margin (%)'},
                            color_discrete_map={'March 2021': '#00BFFF', 'May 2022': '#FF6347'}
                        )
                        
                        fig_overlay.update_layout(
                            xaxis_title="Profit Margin (%)",
                            yaxis_title="Number of Products",
                            height=400,
                            bargap=0.05,
                            bargroupgap=0.1,
                            plot_bgcolor='rgba(30,30,30,0.3)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            margin=dict(l=50, r=50, t=50, b=50),
                            xaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)'),
                            yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.2)')
                        )
                        
                        st.plotly_chart(fig_overlay, use_container_width=True)
                        
                        # Category-wise comparison
                        if 'category' in df_2021.columns and 'category' in df_2022.columns:
                            st.markdown("---")
                            st.markdown("### 📊 Category-wise Margin Comparison")
                            
                            cat_2021 = df_2021.groupby('category')['Profit_Margin_%'].mean().reset_index()
                            cat_2021.columns = ['category', 'March 2021']
                            
                            cat_2022 = df_2022.groupby('category')['Profit_Margin_%'].mean().reset_index()
                            cat_2022.columns = ['category', 'May 2022']
                            
                            # Merge on common categories
                            cat_comparison = cat_2021.merge(cat_2022, on='category', how='inner')
                            
                            if len(cat_comparison) > 0:
                                # Create grouped bar chart
                                fig_cat_compare = go.Figure()
                                
                                fig_cat_compare.add_trace(go.Bar(
                                    x=cat_comparison['category'],
                                    y=cat_comparison['March 2021'],
                                    name='March 2021',
                                    marker_color='#1E90FF'
                                ))
                                
                                fig_cat_compare.add_trace(go.Bar(
                                    x=cat_comparison['category'],
                                    y=cat_comparison['May 2022'],
                                    name='May 2022',
                                    marker_color='#FF4500'
                                ))
                                
                                fig_cat_compare.update_layout(
                                    title='Category-wise Average Profit Margin Comparison',
                                    xaxis_title='Product Category',
                                    yaxis_title='Average Profit Margin (%)',
                                    barmode='group',
                                    xaxis_tickangle=-45,
                                    height=400,
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    margin=dict(l=50, r=50, t=50, b=80)
                                )
                                
                                st.plotly_chart(fig_cat_compare, use_container_width=True)
                                
                                # Show top gainers and losers
                                st.markdown("---")
                                st.markdown("### 🔝 Category Performance Changes")
                                
                                cat_comparison['Change'] = cat_comparison['May 2022'] - cat_comparison['March 2021']
                                cat_comparison = cat_comparison.sort_values('Change', ascending=False)
                                
                                col_gain, col_loss = st.columns(2)
                                
                                with col_gain:
                                    st.markdown("#### 📈 Top Gainers")
                                    top_gainers = cat_comparison.head(5)[['category', 'March 2021', 'May 2022', 'Change']].copy()
                                    top_gainers['Change'] = top_gainers['Change'].apply(lambda x: f"+{x:.2f}%")
                                    top_gainers['March 2021'] = top_gainers['March 2021'].apply(lambda x: f"{x:.2f}%")
                                    top_gainers['May 2022'] = top_gainers['May 2022'].apply(lambda x: f"{x:.2f}%")
                                    st.dataframe(top_gainers, use_container_width=True, hide_index=True)
                                
                                with col_loss:
                                    st.markdown("#### 📉 Top Decliners")
                                    top_losers = cat_comparison.tail(5)[['category', 'March 2021', 'May 2022', 'Change']].copy()
                                    top_losers['Change'] = top_losers['Change'].apply(lambda x: f"{x:.2f}%")
                                    top_losers['March 2021'] = top_losers['March 2021'].apply(lambda x: f"{x:.2f}%")
                                    top_losers['May 2022'] = top_losers['May 2022'].apply(lambda x: f"{x:.2f}%")
                                    st.dataframe(top_losers, use_container_width=True, hide_index=True)
                            else:
                                st.warning("No common categories found for comparison.")
                    
                    except FileNotFoundError as e:
                        st.warning(f"⚠️ Could not load both year files for comparison: {str(e)}")
                        st.info("Please ensure both new_2021_product_info.csv and new_2022_product_info.csv exist in the directory.")
                    except Exception as e:
                        st.error(f"Error in year comparison: {str(e)}")
            
            except FileNotFoundError:
                st.error(f"❌ File not found: {file_name}")
                st.info("Please ensure the file exists in the current directory.")
            except KeyError as e:
                st.error(f"❌ Column not found: {str(e)}")
                st.info(f"Please check that the required columns exist in {file_name}")
            
        except Exception as e:
            st.error(f"❌ Error in Product Profit Margin Analysis: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

if __name__ == "__main__":
    main()