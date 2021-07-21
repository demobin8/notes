```
package cn.test.service.dto;

import lombok.*;

import javax.xml.bind.annotation.XmlRootElement;
import java.io.Serializable;

@Builder
@AllArgsConstructor
@NoArgsConstructor
@XmlRootElement(name = "PaymentResponse")
@Getter
@Setter
@ToString
public class PaymentRespV3 implements Serializable {

    private static final long serialVersionUID = -5685364547551763334L;

    private String timeStamp;
    private String merchantID;
    private String respCode;
    private String amt;
    private String uniqueTransactionCode;
    private String approvalCode;
    private String dateTime;
    private String status;
    private String failReason;
    private String userDefined1;
    private String userDefined2;
    private String userDefined3;

    public static PaymentRespV3 toPaymentRespV3(String xml) {
        return (PaymentRespV3) getResponseBodyObject(xml, PaymentRespV3.class);
    }
	
	public static Object getResponseBodyObject(String xmlStr, Class clazz) {
        Document document = XmlUtil.parseXml(xmlStr);
        String formatXml = XmlUtil.format(document);
        Object xmlObject = null;
        try {
            JAXBContext context = JAXBContext.newInstance(clazz);
            Unmarshaller unmarshaller = context.createUnmarshaller();
            StringReader sr = new StringReader(formatXml);
            xmlObject = unmarshaller.unmarshal(sr);
        } catch (JAXBException e) {
            log.error("exception: {}", e,getMessage());
        }
        return xmlObject;
    }
}
```
