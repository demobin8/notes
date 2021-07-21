> 不要再mapper中定义函数，否则所有同类型的转换全部会调用该方法。。。要开一个类通过imports引用。。。

```
package cn.test.struct;

import cn.test.api.constants.enums.CurrencyCodeEnum;
import cn.test.api.dto.payment.RouterPayment;
import cn.test.api.dto.payment.PaymentTokenRequestParam;
import cn.test.service.dto.PaymentReqV3;
import cn.test.service.dto.PaymentTokenReq;
import cn.test.utils.AmountUtils;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.Mappings;

@Mapper(componentModel = "spring", imports = {AmountUtils.class, CurrencyCodeEnum.class})
public interface PaymentMapper {
    /**
     * param to req
     * @param param param
     * @return req
     */
    @Mappings({@Mapping(target = "invoiceNo", source = "orderId", defaultValue = "")})
    PaymentTokenReq toPaymentTokenReq(PaymentTokenRequestParam param);

    /**
     * param to req v3
     * @param routerPayment p
     * @return req
     */
    @Mappings({
            @Mapping(target = "uniqueTransactionCode", source = "paymentCode", defaultValue = ""),
            @Mapping(target = "amt", expression = "java(AmountUtils.getRealMoney(routerPayment.getMoney().getAmount()))"),
            @Mapping(target = "currencyCode", expression = "java(CurrencyCodeEnum.fromName(routerPayment.getMoney().getCurrency().toUpperCase()).getType())"),
            @Mapping(target = "desc", source = "description", defaultValue = "")})
    PaymentReqV3 toPaymentReqV3(RouterPayment routerPayment);

    /**
     * route to req param
     * @param routerPayment route
     * @return req param
     */
    @Mappings({
            @Mapping(target = "description", expression = "java(routerPayment.getMetadata().get(\"description\"))"),
            @Mapping(target = "orderId", source = "paymentCode", defaultValue = ""),
            @Mapping(target = "payType", expression = "java(routerPayment.getPayType().name())"),
            @Mapping(target = "account", source = "accountCode", defaultValue = ""),
            @Mapping(target = "currency", expression = "java(routerPayment.getMoney().getCurrency().toUpperCase())"),
            @Mapping(target = "amount", expression = "java(AmountUtils.getRealMoney(routerPayment.getMoney().getAmount()))")})
    PaymentTokenRequestParam toPaymentTokenRequestParam(RouterPayment routerPayment);

}

```
