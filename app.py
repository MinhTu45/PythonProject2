import pandas as pd
import streamlit as st
import plotly.express as px
import datetime

# Load the dataset
file_path = "datasets/IMDB Top 250 Movies.csv"
df = pd.read_csv(file_path)

# Sidebar
with st.sidebar:
    st.markdown("Group: **14**")  # Change name of author here
    st.write("Date: ", datetime.date.today())
    st.text("Description: This app analyzes the IMDb Top 250 Movies dataset.")

# Define the available tabs
tabs = ["Cover Page", "Rating Films"]
main_content = st.sidebar.selectbox("Navigation", tabs)

if main_content == "Cover Page":
    # Insert home content here
    st.title("Cover Page")
    # Add more content as needed
        
    # Insert Cover Page
    st.image("images/coverpage.png", use_column_width=True)

    #####################################
    # Contribution list
    # Data
    data = {
        "Name": [
            "Phạm Lê Minh Tú",
            "Huỳnh Ngọc Minh Thư",
            "Huỳnh Lệ Phương",
            "Phạm Thị Thanh Ngân",
            "Nguyễn Anh Phương",
            "Lương Thảo Vy"
        ],
        "Contribution": [
            "Group leader & Web making",
            "Web making",
            "Web making",
            "Web making",
            "Web making",
            "Web making"
        ]
    }


    # Create a DataFrame
    contributionList = pd.DataFrame(data)

    # Display the table in Streamlit
    st.title("Contribution List")
    st.table(contributionList)

    #######################################

    # HTML for the project evaluation table
    html_table = """
    <table style="width:100%; border: 1px solid white; text-align: center;">
        <tr>
            <th colspan="3" style="border: 1px solid white; padding: 10px;">Python Project (45%)</th>
        </tr>
        <tr>
            <td style="border: 1px solid white; padding: 10px;padding-bottom: 200px;">Design (15%)</td>
            <td style="border: 1px solid white; padding: 10px;padding-bottom: 200px;">Content (15%)</td>
            <td style="border: 1px solid white; padding: 10px;padding-bottom: 200px;">Interactive elements (10%)</td>
        </tr>
    </table>
    """
    st.title("Project Evaluation Criteria")
    st.markdown(html_table, unsafe_allow_html=True)


    st.title("Comment")
    st.write("""
            
            
            """)
    #####

else:
    
    # Select the relevant columns
    selected_columns = ['rank', 'name', 'rating', 'genre', 'certificate', 'year', 'budget', 'run_time']
    df_selected = df[selected_columns].copy()

    # Convert budget values to billions
    def convert_to_billions(budget_str):
        if pd.isna(budget_str):
            return None
        budget_str = budget_str.replace('$', '').replace(',', '')
        try:
            budget = float(budget_str)
            return budget / 1e9
        except ValueError:
            return None

    df_selected.loc[:, 'budget'] = df_selected['budget'].apply(convert_to_billions)

    # Create a new DataFrame with split genres
    df_genres_expanded = df_selected.assign(genre=df_selected['genre'].str.split(',')).explode('genre')
    df_genres_expanded['genre'] = df_genres_expanded['genre'].str.strip()


    # Main content
    st.title("Rating Films")
    st.markdown("This application allows you to analyze the IMDb Top 250 Movies dataset.")
    st.divider()

    # Display dataset information
    st.header("Dataset Information")
    st.markdown(
    """
    - **Description**: This dataset stores information about the IMDb Top 250 Movies including their genres, ratings, and other relevant details.
    - **Variables**:
        1. **rank**: The rank of the movie.
        2. **name**: The name of the movie.
        3. **rating**: The IMDb rating of the movie.
        4. **genre**: The genre(s) of the movie.
        5. **certificate**: The certification of the movie.
        6. **year**: The release year of the movie.
        7. **budget**: The budget of the movie (in billions).
        8. **run_time**: The runtime of the movie.
        
        [IMDb Top 250 Movies](https://www.kaggle.com/datasets/yehorkorzh/imdb-top-250-movies)
    """
    )

    # Display the original dataset
    st.dataframe(df_selected, width=1000)


    st.header("Have you ever wondered what people's taste in movies has been over the past century?")
    st.text("Let's check out our website providing the IMDB Top 250 Movies!")

    tab1, tab2 = st.tabs(["General relation", "Trending films in year"])

    with tab1:
        col1, col2 = st.columns([1, 3])

        with col1:
            category_mapping = {
                'genre': 'Genre',
                'budget': 'Budget (in billions)',
                'certificate': 'Certificate',
                'run_time': 'Run Time',
            }
            by_what = st.radio(
                "Choose a category:",
                ['genre', 'budget', 'certificate', 'run_time'],
                format_func=lambda x: category_mapping[x],
                key="r1"
            )
            
            chart_type = st.radio(
                "Choose a chart type:",
                ['Bar Chart', 'Line Chart', 'Scatter Plot', 'Box Plot'],
                key="chart_type"
            )
            
        with col2:
            if chart_type == 'Bar Chart':
                fig = px.bar(df_genres_expanded, x=by_what, y="rating", color=by_what,
                            labels={by_what: category_mapping[by_what], "rating": "Rating"},
                            title=f"Film Rating by {category_mapping[by_what]}")
            elif chart_type == 'Line Chart':
                fig = px.line(df_genres_expanded, x=by_what, y="rating", color=by_what,
                            labels={by_what: category_mapping[by_what], "rating": "Rating"},
                            title=f"Film Rating by {category_mapping[by_what]}")
            elif chart_type == 'Scatter Plot':
                fig = px.scatter(df_genres_expanded, x=by_what, y="rating", color=by_what,
                                labels={by_what: category_mapping[by_what], "rating": "Rating"},
                                title=f"Film Rating by {category_mapping[by_what]}")
            elif chart_type == 'Box Plot':
                fig = px.box(df_genres_expanded, x=by_what, y="rating", color=by_what,
                            labels={by_what: category_mapping[by_what], "rating": "Rating"},
                            title=f"Film Rating by {category_mapping[by_what]}")
            fig.update_layout(
                xaxis=dict(
                    tickangle=-45   
                ),
                showlegend=False
            )
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    #################

    with tab2:
        st.header("Select a range for years:")
        year_range = st.slider("Select a year range:", min_value=1920, max_value=2021, value=(1920, 2021), step=1)
        
        start_year, end_year = year_range
        df_year1 = df_genres_expanded[(df_genres_expanded['year'] >= start_year) & (df_genres_expanded['year'] <= end_year)]
        df_year = df_selected[(df_selected['year'] >= start_year) & (df_selected['year'] <= end_year)]

        st.markdown(f"**Top movies from {start_year} to {end_year}:**")
        st.dataframe(df_year[['rank', 'name', 'rating', 'genre']].head(), width=1000)
        
        popular_genres_year = df_year1['genre'].value_counts().nlargest(10)  # Get top 10 genres for the selected year range
        st.write(f"**Number of Films by Genre from {start_year} to {end_year}:**")
        col1, col2 = st.columns([7, 8])

        with col1:
            if not df_year1.empty:
                fig_year_bar = px.bar(popular_genres_year, x=popular_genres_year.index, y=popular_genres_year.values,
                                    labels={'x': 'Genre', 'y': 'Number of Films'})
                fig_year_bar.update_layout(
                    xaxis=dict(
                        tickangle=-45
                    )
                )
                st.plotly_chart(fig_year_bar, theme="streamlit", use_container_width=True)
            else:
                st.write(f"No films available for the selected range from {start_year} to {end_year}.")
                
        with col2:
            if not df_year1.empty:
                fig_year_pie = px.pie(popular_genres_year, values=popular_genres_year.values, names=popular_genres_year.index)
                
                # Update the layout to place text inside the pie slices
                fig_year_pie.update_traces(textposition='inside', textinfo='percent+label')
                fig_year_pie.update_layout(showlegend=False)

                st.plotly_chart(fig_year_pie, theme="streamlit", use_container_width=True)
            else:
                st.write(f"No films available for the selected range from {start_year} to {end_year}.")
