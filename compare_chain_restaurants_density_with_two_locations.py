from haversine import haversine, Unit, haversine_vector
import pandas as pd

def make_matrix(location, size):
    return [location for i in range(size)]

def dist(d, dist, d1):
    if d1==True:
        if d<=5:
            return 'loc1<='+str(dist)+'km'
        return 'loc1>'+str(dist)+'km'
    else:
        if d<=5:
            return 'loc2<='+str(dist)+'km'
        return 'loc2>'+str(dist)+'km'
    

def main(file, location1, location2):
    osm_data = pd.read_json('clean_osm_data.JSON')
    
    size=osm_data.lat.size
    
    location1_matrix=make_matrix(location1, size)
    location2_matrix=make_matrix(location2, size)
    
    #distance between location 1
    osm_data['dist1']=haversine_vector(
    osm_data[['lat', 'lon']].values.tolist(), [location1 for i in range(size)], 
    Unit.KILOMETERS
    )
    
    #distance between location 2
    osm_data['dist2']=haversine_vector(
        osm_data[['lat', 'lon']].values.tolist(), [location2 for i in range(size)], 
        Unit.KILOMETERS
    )
    
    osm_data['loc1']=osm_data.dist1.apply(dist, dist=5, d1=True)
    osm_data['loc2']=osm_data.dist2.apply(dist, dist=5, d1=False)
    
    group=osm_data.groupby(['name', "loc1"]).count()
    
    loc1=osm_data.groupby(['name', "loc1"]).count().reset_index().pivot(
    index='name', 
    columns='loc1', 
    values='dist1')
    
    loc2=osm_data.groupby(['name', "loc2"]).count().reset_index().pivot(
    index='name', 
    columns='loc2', 
    values='dist2')
    
    loc_cat=pd.concat([loc1, loc2], axis=1)
    loc_cat=loc_cat.sort_values(by=['loc2<=5km', 'loc1<=5km'], ascending=False)
    #print(loc_cat)
    
    #Chi-Squared with the filtered data to compare the density of chain restaurants by two locations
    within_5km=loc_cat[['loc2<=5km', 'loc1<=5km']].sort_values(by=['loc2<=5km', 'loc1<=5km'], ascending=False)
    print(within_5km)
    within_5km.to_json("within_5km.JSON")
    
    
    beyond_5km=loc_cat[['loc2>5km', 'loc1>5km']].sort_values(by=['loc2>5km', 'loc1>5km'], ascending=False)
    #print(beyond_5km)
    



if __name__ == '__main__':
    file='data/amenities-vancouver.json.gz'
    location1 = [49.2768,  -122.9180] #SFU burnaby
    location2 = [49.284478, -123.112349]  #SFU Vancouver
    main(file, location1, location2)