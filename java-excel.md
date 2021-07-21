### 表头定义
```
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class StatisticExcelRecord {

    @ExcelProperty("No.")
    private Long id;

    @ExcelProperty("日期")
    private String date;

    @ExcelProperty("时间")
    private String time;

    @ExcelProperty("交易类型")
    private String businessType;

    @ExcelProperty("订单类型")
    private String orderType;

    @ExcelProperty("关联单ID")
    private String orderAlias;

    @ExcelProperty("流水动作")
    private String action;

    @ExcelProperty("流水ID")
    private String billCode;

    @ExcelProperty("用户总计")
    private String customerTotalAmount;
}

```
### mapstruct
```
@Mapper(componentModel = "spring", imports = {DateFormatUtils.class, BusinessTypeEnum.class)
public interface StatisticExcelMapper {

    @Mappings({
            @Mapping(target = "date", expression = "java(DateFormatUtils.formatWithHorizontalBar(info.getTransactionTime()))"),
            @Mapping(target = "time", expression = "java(DateFormatUtils.formatTimeWithColon(info.getTransactionTime()))"),
            @Mapping(target = "businessType", expression = "java(info.getBusinessType().getDescription())"),
            @Mapping(target = "orderType", expression = "java(info.getOrderType().getDescription())")
    })
    StatisticExcelRecord toStatisticExcelRecord(StatisticinfoVO info, String url);

}

```
### write excel
```
...
        EasyExcel.write(path, StatisticExcelRecord.class).sheet(filename).registerWriteHandler(new CustomCellWriteHandler()).doWrite(statisticExcelRecordList);
```
### CustomCellWriteHandler
```
@Service
public class CustomCellWriteHandler extends AbstractColumnWidthStyleStrategy {
    private final Map<Integer, Map<Integer, Integer>> CACHE = new HashMap<>();

    @Override
    protected void setColumnWidth(WriteSheetHolder writeSheetHolder, List<CellData> cellDataList, Cell cell, Head head, Integer relativeRowIndex, Boolean isHead) {
	
        boolean needSetWidth = isHead || !CollectionUtils.isEmpty(cellDataList);
		
        if (needSetWidth) {
            Map<Integer, Integer> maxColumnWidthMap = CACHE.computeIfAbsent(writeSheetHolder.getSheetNo(), k -> new HashMap<>());

            Integer columnWidth = this.dataLength(cellDataList, cell, isHead);
            if (columnWidth >= 0) {
                if (columnWidth > 255) {
                    columnWidth = 255;
                }

                Integer maxColumnWidth = maxColumnWidthMap.get(cell.getColumnIndex());
                if (maxColumnWidth == null || columnWidth > maxColumnWidth) {
                    maxColumnWidthMap.put(cell.getColumnIndex(), columnWidth);
                    writeSheetHolder.getSheet().setColumnWidth(cell.getColumnIndex(), columnWidth * 256);
                }

            }
        }
    }

    private Integer dataLength(List<CellData> cellDataList, Cell cell, Boolean isHead) {
	
        if (isHead) {
            return cell.getStringCellValue().getBytes().length;
        }
		
		CellData cellData = cellDataList.get(0);
		CellDataTypeEnum type = cellData.getType();
		if (type == null) {
			return -1;
		}
		
		switch (type) {
			case STRING:
				return cellData.getStringValue().getBytes().length + 3;
			case BOOLEAN:
				return cellData.getBooleanValue().toString().getBytes().length + 3;
			case NUMBER:
				return cellData.getNumberValue().toString().getBytes().length + 3;
			default:
				return -1;
		}
    }
}

```
