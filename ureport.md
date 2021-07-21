### data source config
```
package cn.test.demobin;

import com.bstek.ureport.definition.datasource.BuildinDatasource;
import lombok.extern.log4j.Log4j2;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.SQLException;

@Log4j2
@Component
public class UReportDataSource implements BuildinDatasource {

    private static final String datasourceName = "uReportDatasource";
    @Autowired
    private DataSource dataSource;

    @Override
    public String name() {
        return datasourceName;
    }

    @Override
    public Connection getConnection() {
        try{
            return dataSource.getConnection();
        } catch (SQLException e) {
            log.error("uReport2 datasource get connection failed");
            e.printStackTrace();
        }
        return null;
    }
}
```

### properties
```
ureport.debug=true
ureport.fileStoreDir=/home/demobin/report
ureport.disableHttpSessionReportCache=true
ureport.disableFileProvider=false
```

### report.xml
```
<?xml version="1.0" encoding="UTF-8"?><ureport><cell expand="None" name="A1" row="1" col="1" col-span="4"><cell-style font-size="20" forecolor="0,0,0" font-family="微软雅黑" align="center" valign="middle" line-height="2"><left-border width="1" style="solid" color="0,0,0"/><right-border width="1" style="solid" color="0,0,0"/><top-border width="1" style="solid" color="0,0,0"/><bottom-border width="1" style="solid" color="0,0,0"/></cell-style><simple-value><![CDATA[Silicon PV Module]]></simple-value></cell><cell expand="None" name="A2" row="2" col="1"><cell-style font-size="12" forecolor="0,0,0" font-family="宋体" align="center" valign="middle" line-height="2"><left-border width="1" style="solid" color="0,0,0"/><right-border width="1" style="solid" color="0,0,0"/><top-border width="1" style="solid" color="0,0,0"/><bottom-border width="1" style="solid" color="0,0,0"/></cell-style><simple-value><![CDATA[Type]]></simple-value></cell><cell expand="None" name="B2" row="2" col="2" col-span="3"><cell-style font-size="12" forecolor="0,0,0" font-family="宋体" align="center" valign="middle"><left-border width="1" style="solid" color="0,0,0"/><right-border width="1" style="solid" color="0,0,0"/><top-border width="1" style="solid" color="0,0,0"/><bottom-border width="1" style="solid" color="0,0,0"/></cell-style><dataset-value dataset-name="request" aggregate="group" property="Type" order="none" mapping-type="simple"></dataset-value></cell><cell expand="None" name="A3" row="3" col="1"><cell-style font-size="12" forecolor="0,0,0" font-family="宋体" align="center" valign="middle"><left-border width="1" style="solid" color="0,0,0"/><right-border width="1" style="solid" color="0,0,0"/><top-border width="1" style="solid" color="0,0,0"/><bottom-border width="1" style="solid" color="0,0,0"/></cell-style><simple-value><![CDATA[Grade]]></simple-value></cell><cell expand="None" name="B3" row="3" col="2"><cell-style font-size="12" forecolor="0,0,0" font-family="宋体" align="center" valign="middle"><left-border width="1" style="solid" color="0,0,0"/><right-border width="1" style="solid" color="0,0,0"/><top-border width="1" style="solid" color="0,0,0"/><bottom-border width="1" style="solid" color="0,0,0"/></cell-style><dataset-value dataset-name="request" aggregate="group" property="Grade" order="none" mapping-type="simple"></dataset-value></cell><cell expand="None" name="C3" row="3" col="3"><cell-style font-size="12" forecolor="0,0,0" font-family="宋体" align="center" valign="middle"><left-border width="1" style="solid" color="0,0,0"/><right-border width="1" style="solid" color="0,0,0"/><top-border width="1" style="solid" color="0,0,0"/><bottom-border width="1" style="solid" color="0,0,0"/></cell-style><simple-value><![CDATA[Qty.]]></simple-value></cell><cell expand="None" name="D3" row="3" col="4"><cell-style font-size="12" forecolor="0,0,0" font-family="宋体" align="center" valign="middle"><left-border width="1" style="solid" color="0,0,0"/><right-border width="1" style="solid" color="0,0,0"/><top-border width="1" style="solid" color="0,0,0"/><bottom-border width="1" style="solid" color="0,0,0"/></cell-style><dataset-value dataset-name="request" aggregate="group" property="Qty" order="none" mapping-type="simple"></dataset-value></cell><cell expand="None" name="A4" row="4" col="1" col-span="4"><cell-style font-size="20" forecolor="0,0,0" font-family="宋体" align="center" valign="middle"><left-border width="1" style="solid" color="0,0,0"/><right-border width="1" style="solid" color="0,0,0"/><top-border width="1" style="solid" color="0,0,0"/><bottom-border width="1" style="solid" color="0,0,0"/></cell-style><dataset-value dataset-name="request" aggregate="group" property="palletNo" order="none" mapping-type="simple"></dataset-value></cell><cell expand="None" name="A5" row="5" col="1"><cell-style font-size="12" forecolor="0,0,0" font-family="宋体" align="center" valign="middle"><left-border width="1" style="solid" color="0,0,0"/><right-border width="1" style="solid" color="0,0,0"/><top-border width="1" style="solid" color="0,0,0"/><bottom-border width="1" style="solid" color="0,0,0"/></cell-style><simple-value><![CDATA[LOT NO.]]></simple-value></cell><cell expand="None" name="B5" row="5" col="2" col-span="3"><cell-style font-size="12" forecolor="0,0,0" font-family="宋体" align="center" valign="middle"><left-border width="1" style="solid" color="0,0,0"/><right-border width="1" style="solid" color="0,0,0"/><top-border width="1" style="solid" color="0,0,0"/><bottom-border width="1" style="solid" color="0,0,0"/></cell-style><dataset-value dataset-name="request" aggregate="group" property="LOTNO" order="none" mapping-type="simple"></dataset-value></cell><cell expand="None" name="A6" row="6" col="1"><cell-style font-size="12" forecolor="0,0,0" font-family="宋体" align="center" valign="middle"><left-border width="1" style="solid" color="0,0,0"/><right-border width="1" style="solid" color="0,0,0"/><top-border width="1" style="solid" color="0,0,0"/><bottom-border width="1" style="solid" color="0,0,0"/></cell-style><simple-value><![CDATA[Client]]></simple-value></cell><cell expand="None" name="B6" row="6" col="2" col-span="3"><cell-style font-size="9" forecolor="0,0,0" font-family="宋体" align="center" valign="middle"><left-border width="1" style="solid" color="0,0,0"/><right-border width="1" style="solid" color="0,0,0"/><top-border width="1" style="solid" color="0,0,0"/><bottom-border width="1" style="solid" color="0,0,0"/></cell-style><simple-value><![CDATA[]]></simple-value></cell><cell expand="None" name="A7" row="7" col="1"><cell-style font-size="12" forecolor="0,0,0" font-family="宋体" align="center" valign="middle" line-height="3"><left-border width="1" style="solid" color="0,0,0"/><right-border width="1" style="solid" color="0,0,0"/><top-border width="1" style="solid" color="0,0,0"/><bottom-border width="1" style="solid" color="0,0,0"/></cell-style><simple-value><![CDATA[Pallet NO.]]></simple-value></cell><cell expand="None" name="B7" row="7" col="2" col-span="3"><cell-style font-size="9" forecolor="0,0,0" font-family="宋体" align="center" valign="middle"><left-border width="1" style="solid" color="0,0,0"/><right-border width="1" style="solid" color="0,0,0"/><top-border width="1" style="solid" color="0,0,0"/><bottom-border width="1" style="solid" color="0,0,0"/></cell-style><zxing-value source="expression" category="barcode" width="120" height="40" format="CODE_128"><text><![CDATA[A4]]></text></zxing-value></cell><cell expand="Down" name="A8" row="8" col="1" col-span="2"><cell-style font-size="12" forecolor="0,0,0" font-family="宋体" align="center" valign="middle" line-height="1.5"><left-border width="1" style="solid" color="0,0,0"/><right-border width="1" style="solid" color="0,0,0"/><top-border width="1" style="solid" color="0,0,0"/><bottom-border width="1" style="solid" color="0,0,0"/></cell-style><dataset-value dataset-name="component" aggregate="select" property="snr" order="none" mapping-type="simple"></dataset-value></cell><cell expand="Down" name="C8" row="8" col="3" col-span="2"><cell-style font-size="9" forecolor="0,0,0" font-family="宋体" align="center" valign="middle"><left-border width="1" style="solid" color="0,0,0"/><right-border width="1" style="solid" color="0,0,0"/><top-border width="1" style="solid" color="0,0,0"/><bottom-border width="1" style="solid" color="0,0,0"/></cell-style><zxing-value source="expression" category="barcode" width="120" height="20" format="CODE_128"><text><![CDATA[A8]]></text></zxing-value></cell><row row-number="1" height="19"/><row row-number="2" height="19"/><row row-number="3" height="19"/><row row-number="4" height="19"/><row row-number="5" height="19"/><row row-number="6" height="19"/><row row-number="7" height="19"/><row row-number="8" height="19"/><column col-number="1" width="97"/><column col-number="2" width="97"/><column col-number="3" width="97"/><column col-number="4" width="97"/><datasource name="uReportDatasource" type="buildin"><dataset name="component1" type="sql"><sql><![CDATA[SELECT
	S.snr 
FROM
	(
	SELECT
		U2.*,
		@RN := @RN + 1 ROWNUMBER,
		(
		SELECT
			ROUND( COUNT( * ) / 2 ) 
		FROM
			pallet_component p
			LEFT JOIN component U ON U.component_id = p.component_id 
		WHERE
			p.pallet_id = 2 
		) TOPN 
	FROM
		pallet_component p2
		LEFT JOIN component U2 ON U2.component_id = p2.component_id
		CROSS JOIN ( SELECT @RN := 0 ) R 
	WHERE
		p2.pallet_id = :palletId
	ORDER BY
		component_id 
	) S 
WHERE
	S.ROWNUMBER <= S.TOPN;]]></sql><field name="snr"/><parameter name="palletId" type="Integer" default-value="2"/></dataset><dataset name="request" type="sql"><sql><![CDATA[SELECT
  p.pallet_no as 'palletNo',
	MAX(CASE rpt_setting_key WHEN 'Type' THEN rpt_setting_value ELSE 0 END) AS 'Type' ,
	MAX(CASE rpt_setting_key WHEN 'Qty' THEN rpt_setting_value ELSE 0 END) AS 'Qty' ,
	MAX(CASE rpt_setting_key WHEN 'LOTNO' THEN rpt_setting_value ELSE 0 END) AS 'LOTNO' ,
    MAX(CASE rpt_setting_key WHEN 'Remark' THEN rpt_setting_value ELSE 0 END) AS 'Remark' ,
	MAX(CASE rpt_setting_key WHEN 'Grade' THEN rpt_setting_value ELSE 0 END) AS 'Grade' 
FROM
	report_setting
LEFT JOIN pallet p ON p.pallet_id = :palletId
WHERE
	report_id = :reportId
GROUP BY
	report_id;]]></sql><field name="palletNo"/><field name="Type"/><field name="Qty"/><field name="LOTNO"/><field name="Remark"/><field name="Grade"/><parameter name="reportId" type="String" default-value="2"/><parameter name="palletId" type="String" default-value="2"/></dataset><dataset name="component2" type="sql"><sql><![CDATA[SELECT
	S.snr 
FROM
	(
	SELECT
		U2.*,
		@RN := @RN + 1 ROWNUMBER,
		(
		SELECT
			ROUND( COUNT( * ) / 2 ) 
		FROM
			pallet_component p
			LEFT JOIN component U ON U.component_id = p.component_id 
		WHERE
			p.pallet_id = 2 
		) TOPN 
	FROM
		pallet_component p2
		LEFT JOIN component U2 ON U2.component_id = p2.component_id
		CROSS JOIN ( SELECT @RN := 0 ) R 
	WHERE
		p2.pallet_id = :palletId
	ORDER BY
		component_id 
	) S 
WHERE
	S.ROWNUMBER > S.TOPN;]]></sql><field name="snr"/><parameter name="palletId" type="String" default-value="2"/></dataset><dataset name="component" type="sql"><sql><![CDATA[select c.snr from pallet_component pc left join component c on pc.component_id=c.component_id where pc.pallet_id=:palletId]]></sql><field name="snr"/><parameter name="palletId" type="String" default-value="2"/></dataset></datasource><paper type="A4" left-margin="90" right-margin="90"
    top-margin="72" bottom-margin="72" paging-mode="fitpage" fixrows="0"
    width="595" height="842" orientation="portrait" html-report-align="left" bg-image="" html-interval-refresh-value="0" column-enabled="false"></paper><search-form form-position="down"/></ureport>
```
