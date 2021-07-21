### GeoApiContext
```
@Slf4j
@Data
@Component
public class GoogleApiContext {
  
    private static String ENABL_PROXY = "Y";

    @Value("${google.proxy.apiKey:key}")
    private static String apiKey;
    @Value("${google.proxy.hostName:192.168.1.2}")
    private static String hostName;
    @Value("${google.proxy.port:3128}")
    private static int port;

    private static volatile GeoApiContext instance;

    public static GeoApiContext getInstance() {
        if (instance == null)
            synchronized (cn.test.map.GoogleApiContext.class) {
                if (instance == null)
                    instance = (new GeoApiContext.Builder()).apiKey(apiKey).proxy(new Proxy(Proxy.Type.HTTP, new InetSocketAddress(hostName, port))).build();
            }
        return instance;
    }
  
}
```
### DTO
LatAndLonDTO
```
@Data
@Builder
@ToString
@AllArgsConstructor
@ApiModel("LatAndLonDTO")
public class LatAndLonDTO implements Serializable {

    private static final long serialVersionUID = 119260181358176687L;

    @ApiModelProperty(value = "经度",required = true)
    @NotEmpty
    @NotNull(message = "经度不能为空")
    private String longitude;

    @ApiModelProperty(value = "纬度",required = true)
    @NotEmpty
    @NotNull(message = "纬度不能为空")
    private String latitude;

    @Tolerate
    public LatAndLonDTO(){}
}

```
DirectionsDTO
```
@Data
@Builder
@ToString
@AllArgsConstructor
@ApiModel("DirectionsDTO")
public class DirectionsDTO implements Serializable {
  private static final long serialVersionUID = 8607618469659620418L;
  
  @ApiModelProperty(value = "起点经度", required = true)
  @NotEmpty
  @NotNull(message = "起点经度不能为空")
  private String startLat;
  
  @ApiModelProperty(value = "起点纬度", required = true)
  @NotEmpty
  @NotNull(message = "起点纬度不能为空")
  private String startLng;
  
  @ApiModelProperty(value = "终点经度", required = true)
  @NotEmpty
  @NotNull(message = "终点经度不能为空")
  private String endLat;
  
  @ApiModelProperty(value = "终点纬度", required = true)
  @NotEmpty
  @NotNull(message = "终点纬度不能为空")
  private String endLng;
  
  @ApiModelProperty("中间节点经纬度")
  private LatLng midLatLng;
  
  private String region;
}
```
NearSearchDTO
```
@Data
@Builder
@ToString
@AllArgsConstructor
@ApiModel("NearSearchDTO")
public class NearSearchDTO implements Serializable {
    private static final long serialVersionUID = -1604171566642471515L;

    @ApiModelProperty("搜索框输入值")
    @JsonStringTrimFormat
    private String keyWord;

    @ApiModelProperty(value = "经度", required = true)
    @NotEmpty
    @NotNull(message = "经度不能为空")
    private String longitude;

    @ApiModelProperty(value = "纬度", required = true)
    @NotEmpty
    @NotNull(message = "纬度不能为空")
    private String latitude;

    @ApiModelProperty("半径")
    private Integer radius;
}
```
### GeocodingApi, PlacesApi, DirectionsApi
```
    public String getCity(LatAndLonDTO latAndLon, String language) {

        if (latAndLon.getAddressTypes() == null || (latAndLon.getAddressTypes()).length == 0) {
            AddressType[] addressTypes = { AddressType.POLITICAL };
            latAndLon.setAddressTypes(addressTypes);
        }

        GeocodingResult[] geocode = geocode(latAndLon, latAndLon.getAddressTypes(), language);

        if (ArrayUtils.isEmpty((Object[])geocode))
            return null;

        for (GeocodingResult result : geocode) {
            for (AddressComponent addressComponent : result.addressComponents) {
                for (AddressComponentType type : addressComponent.types) {
                    if (StringUtils.equalsIgnoreCase(type.toString(), "locality"))
                        return addressComponent.longName;
                }
            }
        }

        return null;
    }


    public DirectionsResult directionsResult(DirectionsDTO dto, String language) {
        LatLng start = new LatLng();
        LatLng end = new LatLng();
		
        try {
            start = new LatLng((new BigDecimal(dto.getStartLat())).doubleValue(), (new BigDecimal(dto.getStartLng())).doubleValue());
            end = new LatLng((new BigDecimal(dto.getEndLat())).doubleValue(), (new BigDecimal(dto.getEndLng())).doubleValue());
        } catch (Exception e) {
            throw new ServiceException(MapResultCode.API_ERROR);
        }
		
        DirectionsResult result = null;
        try {
            if (dto.getMidLatLng() == null) {
                result = (DirectionsResult)((DirectionsApiRequest)DirectionsApi.newRequest(GoogleApiContext.getInstance()).mode(TravelMode.WALKING).units(Unit.METRIC).region(dto.getRegion()).origin(start).destination(end).language(language)).await();
            } else {
                result = (DirectionsResult)((DirectionsApiRequest)DirectionsApi.newRequest(GoogleApiContext.getInstance()).mode(TravelMode.WALKING).units(Unit.METRIC).region(dto.getRegion()).origin(start).destination(end).waypoints(new LatLng[] { dto.getMidLatLng() }).language(language)).await();
            }
        } catch (Exception e) {
            throw new ServiceException(MapResultCode.API_ERROR);
        }

        return result;
    }


    public PlacesSearchResponse nearSearch(NearSearchDTO dto, String language) {

        LatLng location = new LatLng((new BigDecimal(dto.getLatitude())).doubleValue(), (new BigDecimal(dto.getLongitude())).doubleValue());

        PlacesSearchResponse result = null;

        if (dto.getRadius() == null || dto.getRadius().intValue() <= 0 || dto.getRadius().intValue() > 10000)
            throw new ServiceException(MapResultCode.RADIUS_ERROR);

        try {
            if (StringUtils.isNotBlank(dto.getKeyWord())) {

                result = (PlacesSearchResponse)((NearbySearchRequest)PlacesApi.nearbySearchQuery(GoogleApiContext.getInstance(), location).keyword(dto.getKeyWord()).radius(dto.getRadius().intValue()).rankby(RankBy.PROMINENCE).language(language)).await();

            } else {

                result = (PlacesSearchResponse)((NearbySearchRequest)PlacesApi.nearbySearchQuery(GoogleApiContext.getInstance(), location).radius(dto.getRadius().intValue()).rankby(RankBy.PROMINENCE).language(language)).await();

            }

            orderSearch(result, location, dto.getRadius());

        } catch (ApiException | InterruptedException | IOException e) {
            throw new ServiceException(MapResultCode.API_ERROR);
        }

        return result;
    }

    private void orderSearch(PlacesSearchResponse result, LatLng location, Integer radius) {
    
        if (result == null || result.results == null) {
            return;
        }
        
        Map<String, PlacesSearchResult> placesMap = new HashMap<>();
        Map<String, Integer> distanceMap = new HashMap<>();

        PlacesSearchResult[] placesSearchResults = new PlacesSearchResult[result.results.length];

        for (PlacesSearchResult searchResult : result.results) {
            LatLng latLng = searchResult.geometry.location;
            String key = latLng.lat + "_" + latLng.lng;
			
            Integer distance = getDistance(latLng.lat, latLng.lng, location.lat, location.lng);
			
            if (distance.intValue() <= radius.intValue()) {
                placesMap.put(key, searchResult);
                distanceMap.put(key, distance);
            }
        }
        
        distanceMap = sortByValue(distanceMap);

        int index = 0;
        for (Map.Entry<String, Integer> entry : distanceMap.entrySet()) {
            placesSearchResults[index] = placesMap.get(entry.getKey());
            index++;
        }

        result.results = placesSearchResults;
    }

    public static GeocodingResult[] geocode(LatAndLonDTO latAndLon, AddressType[] resultTypes, String language) {
    
        LatLng location;
        if (StringUtils.isEmpty(latAndLon.getLatitude()) || StringUtils.isEmpty(latAndLon.getLongitude()))
            return null;
            
        try {
            location = new LatLng((new BigDecimal(latAndLon.getLatitude())).doubleValue(), (new BigDecimal(latAndLon.getLongitude())).doubleValue());
        } catch (Exception e) {
            throw new ServiceException(MapResultCode.API_ERROR);
        }
        
        GeocodingResult[] results = null;
        
        try {
            GeocodingApiRequest geocodingApiRequest = (GeocodingApiRequest)GeocodingApi.newRequest(GoogleApiContext.getInstance()).latlng(location).language(language);
            
            if (resultTypes != null && resultTypes.length > 0)
                geocodingApiRequest.resultType(resultTypes);
            results = (GeocodingResult[])geocodingApiRequest.await();
        } catch (Exception e) {
            throw new ServiceException(MapResultCode.API_ERROR);
        }
        
        return results;
    }

    public static <K, V extends Comparable<? super V>> Map<K, V> sortByValue(Map<K, V> map) {
        Map<K, V> result = new LinkedHashMap<>();
        map.entrySet()
                .stream()
                .sorted(Map.Entry.comparingByValue())
                .forEachOrdered(e -> (Comparable)result.put(e.getKey(), e.getValue()));
        return result;
    }
	    private static double rad(double d) {
        return d * Math.PI / 180.0D;
    }

    private static double EARTH_RADIUS = 6378.137D;

    public static Integer getDistance(double lat1, double lng1, double lat2, double lng2) {
        double radLat1 = rad(lat1);
        double radLat2 = rad(lat2);
        double a = radLat1 - radLat2;
        double b = rad(lng1) - rad(lng2);
        double s = 2.0D * Math.asin(Math.sqrt(Math.pow(Math.sin(a / 2.0D), 2.0D) + Math.cos(radLat1) * Math.cos(radLat2) * Math.pow(Math.sin(b / 2.0D), 2.0D)));
        s *= EARTH_RADIUS;
        s *= 1000.0D;
        DecimalFormat df = new DecimalFormat("0");
        String distance = df.format(s);
        return Integer.parseInt(distance);
    }
```
