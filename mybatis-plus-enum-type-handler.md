
### handler
```
package cn.test.payment.config;

import cn.test.payment.constant.IEnum;
import org.apache.ibatis.type.BaseTypeHandler;
import org.apache.ibatis.type.JdbcType;
import java.sql.CallableStatement;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Map;

public class EnumCodeTypeHandler<E extends IEnum> extends BaseTypeHandler<E> {
    private final Class<E> type;
    private final Map<Integer, E> map = new HashMap<>();
    /**
    * 构造函数
    *
    * @param type
    */
    public EnumCodeTypeHandler(Class<E> type) {
        if (type == null) {
            throw new IllegalArgumentException("Type argument cannot be null");
        }
        this.type = type;
        E[] enums = type.getEnumConstants();
        if (enums == null) {
            throw new IllegalArgumentException(type.getSimpleName() + " does not represent an enum type.");
        }
        for (E anEnum : enums) {
            map.put(anEnum.code(), anEnum);
        }
    }
    @Override
    public void setNonNullParameter(PreparedStatement ps, int i, E parameter, JdbcType jdbcType) throws SQLException {
        ps.setInt(i, parameter.code());
    }
    @Override
    public E getNullableResult(ResultSet rs, String columnName) throws SQLException {
        int i = rs.getInt(columnName);
        if (i == 0 && rs.wasNull()) {
            return null;
        } else {
            try {
                return toEnum(i);
            } catch (Exception ex) {
                throw new IllegalArgumentException(
                    "Cannot convert " + i + " to " + type.getSimpleName() + " by ordinal value.", ex);
            }
        }
    }
    @Override
    public E getNullableResult(ResultSet rs, int columnIndex) throws SQLException {
        int i = rs.getInt(columnIndex);
        if (i == 0 && rs.wasNull()) {
            return null;
        } else {
            try {
                return toEnum(i);
            } catch (Exception ex) {
                throw new IllegalArgumentException(
                    "Cannot convert " + i + " to " + type.getSimpleName() + " by ordinal value.", ex);
            }
        }
    }
    @Override
    public E getNullableResult(CallableStatement cs, int columnIndex) throws SQLException {
        int i = cs.getInt(columnIndex);
        if (i == 0 && cs.wasNull()) {
            return null;
        } else {
            try {
                return toEnum(i);
            } catch (Exception ex) {
                throw new IllegalArgumentException(
                    "Cannot convert " + i + " to " + type.getSimpleName() + " by ordinal value.", ex);
            }
        }
    }
    /**
    * code转换为枚举对象
    *
    * @param code
    * @return
    */
    private E toEnum(int code) {
        return map.get(code);
    }
}
```

### bootstrap.yaml
```
mybatis-plus:
  configuration:
    default-enum-type-handler: cn.test.payment.config.EnumCodeTypeHandler
```
