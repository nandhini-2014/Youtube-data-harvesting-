# import sqlalchemy
import pandas as pd
import streamlit as st
import pymysql

# # Connect to the database
# engine=sqlalchemy.create_engine
# db_host='database-1.cti84aqieagm.us-east-2.rds.amazonaws.com'
# db_user='Mugi'
# db_password='rootroot'
# db_name='youtube'
# connection_url=f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"
# engine=sqlalchemy.create_engine(connection_url)
# connection=engine.connect()
st.title("YOUTUBE DATA HARVESTING")
# question = st.text_input('Enter ur question:')

# Establish connection to the databasse
connection = pymysql.connect(
    host='database-1.cti84aqieagm.us-east-2.rds.amazonaws.com',
    user='Mugi',
    password='rootroot',
    database='youtube'
)


# my_question = 'Which channels have the most number of videos, and how many videos do they have?'
queries = {
    'Question 1': """
        SELECT vd.Title AS Video_Title, cd.Channel_Name
        FROM video_details vd
        JOIN channel_details cd ON vd.Channel_Id = cd.Channel_Id
        ORDER BY vd.Views DESC
        LIMIT 10;""",
        
    'Question 2': """
        SELECT vd.Title AS Video_Title, cd.Channel_Name, vd.Views
        FROM video_details vd
        JOIN channel_details cd ON vd.Channel_Id = cd.Channel_Id
        ORDER BY vd.Views DESC
        LIMIT 10;""",
        
    'Question 3': """
        SELECT vd.Title AS Video_Title, 
        COUNT(cd.Comment_Id) AS Number_of_Comments
        FROM video_details vd
        JOIN comment_details cd ON vd.Video_Id = cd.Video_Id
        GROUP BY vd.Video_Id, vd.Title;""",
        
    'Question 4': """
        SELECT vd.Title AS Video_Title, cd.Channel_Name, vd.Favorite_Count AS Likes
        FROM video_details vd
        JOIN channel_details cd ON vd.Channel_Id = cd.Channel_Id
        ORDER BY vd.Favorite_Count DESC
        LIMIT 10;""",
        
    'Question 5': """
        SELECT cd.Channel_Name, 
        SUM(vd.Views) AS Total_Views
        FROM video_details vd
        JOIN channel_details cd ON vd.Channel_Id = cd.Channel_Id
        GROUP BY cd.Channel_Id, cd.Channel_Name;""",
    'Question 6': """
        SELECT DISTINCT cd.Channel_Name
        FROM video_details vd
        JOIN channel_details cd ON vd.Channel_Id = cd.Channel_Id
        WHERE YEAR(vd.Published_Date) = 2024;""",
    'Question 7': """
        SELECT cd.Channel_Name, 
        AVG(TIME_TO_SEC(vd.Duration)) AS Average_Duration
        FROM video_details vd
        JOIN channel_details cd ON vd.Channel_Id = cd.Channel_Id
        GROUP BY cd.Channel_Name;""",
    'Question 8': """
        SELECT vd.Title AS Video_Title, 
        cd.Channel_Name, 
        vd.Comments AS Number_of_Comments
        FROM video_details vd
        JOIN channel_details cd ON vd.Channel_Id = cd.Channel_Id""",
    'Question 9': """
        SELECT Channel_Name, Total_Videos
        FROM channel_details
        ORDER BY Total_Videos DESC;"""
    }

# Get user selected question from the dropdown
selected_question = st.selectbox('Select a question:', list(queries.keys()))

if st.button('Submit'):
    if selected_question in queries:
        try:
            with connection.cursor() as cursor:
                # SQL query to retrieve video names and their corresponding channels
                # if question == my_question:

                cursor.execute(queries[selected_question])
                
                # Fetch column names from the cursor description
                column_names = [desc[0] for desc in cursor.description]
                
                # Fetch all the results
                results = cursor.fetchall()

                # Convert results to DataFrame
                df = pd.DataFrame(results, columns=column_names)

                # Display the results as a table in Streamlit
                st.table(df)
                

                
                
                # Execute the SQL query
                
        finally:
            # Close the connection
            connection.close()

    else:
        st.write("Write your question properly")
    