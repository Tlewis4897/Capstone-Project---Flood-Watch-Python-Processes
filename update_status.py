def update_gauge_status(gauges,status,cursor):
    for gaugeid in gauges:
        query = f'''
        update [HarrisburgWarningSystem].[dbo].[GAUGES]
            set status = '{status}'
            where gauge_id = '{gaugeid}' 
            '''
        cursor.execute(query)
        cursor.commit()