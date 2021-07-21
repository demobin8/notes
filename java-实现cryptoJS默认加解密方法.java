//https://stackoverflow.com/questions/41432896/cryptojs-aes-encryption-and-java-aes-decryption

package cn.test.utils;

import lombok.extern.slf4j.Slf4j;
import org.bouncycastle.util.encoders.Base64;

import javax.crypto.*;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.*;
import java.security.spec.X509EncodedKeySpec;
import java.util.Arrays;
import java.util.Random;

@Slf4j
public class CcppEncryptAlgorithmUtils {

    public static String KEY = "your-key";

    public static Integer AES_SALT_LENGTH = 8;
    public static Integer AES_KEY_LENGTH = 32;
    public static Integer AES_IV_LENGTH = 16;
    public static Integer AES_ITERATION = 1;

    public static String buildSecretToken(String card, String month, String year, String cvv){
        String info = card + ";" + month + ";" + year + ";" + cvv;
        String pass = getRandomString(8);
        try {
            String rsa = encryptByRsa(pass, KEY);
            String aes = encryptByAes(pass, info);
            String rsaLengthPre = Integer.toHexString(rsa.length());
            for (int i = rsaLengthPre.length(); i < 4; i ++){
                rsaLengthPre = "0" + rsaLengthPre;
            }
            return rsaLengthPre + rsa + aes;
        } catch (Exception e) {
            log.error("secret token generate failed: {} - {}", info, e.getMessage());
            e.printStackTrace();
        }
        return null;
    }

    public static String encryptByRsa(String password, String publicKey) throws Exception{
        //base64编码的公钥
        byte[] decoded = Base64.decode(publicKey);;

        KeyFactory kf = KeyFactory.getInstance("RSA");
        PublicKey pubKey = kf.generatePublic(new X509EncodedKeySpec(decoded));

        //RSA加密
        Cipher cipher = Cipher.getInstance("RSA");
        cipher.init(Cipher.ENCRYPT_MODE, pubKey);

        return Base64.toBase64String(cipher.doFinal(password.getBytes(StandardCharsets.UTF_8)));
    }

    public static String encryptByAes(String secret, String plainText) throws NoSuchAlgorithmException, NoSuchPaddingException, InvalidAlgorithmParameterException, InvalidKeyException, BadPaddingException, IllegalBlockSizeException {

        byte[] saltPre = "Salted__".getBytes();
        byte[] saltAft = getRandomString(AES_SALT_LENGTH).getBytes(StandardCharsets.UTF_8);
        byte[] salt = new byte[saltPre.length + saltAft.length];
        System.arraycopy(saltPre, 0, salt, 0, saltPre.length);
        System.arraycopy(saltAft, 0, salt, saltPre.length, saltAft.length);

        MessageDigest md5 = MessageDigest.getInstance("MD5");
        final byte[][] keyAndIv = generateKeyAndIv(AES_KEY_LENGTH, AES_IV_LENGTH, AES_ITERATION, saltAft, secret.getBytes(StandardCharsets.UTF_8), md5);
        SecretKeySpec key = new SecretKeySpec(keyAndIv[0], "AES");
        IvParameterSpec iv = new IvParameterSpec(keyAndIv[1]);

        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, key, iv);
        byte[] cipherText = cipher.doFinal(plainText.getBytes(StandardCharsets.UTF_8));

        byte[] rst = new byte[salt.length + cipherText.length];
        System.arraycopy(salt, 0, rst, 0, salt.length);
        System.arraycopy(cipherText, 0, rst, salt.length, cipherText.length);

        return Base64.toBase64String(rst);
    }

    public static String decryptByAes(String secret, String cipherText) throws NoSuchAlgorithmException, NoSuchPaddingException, InvalidAlgorithmParameterException, InvalidKeyException, BadPaddingException, IllegalBlockSizeException {

        byte[] cipherData = Base64.decode(cipherText);
        byte[] saltData = Arrays.copyOfRange(cipherData, 8, 16);

        MessageDigest md5 = MessageDigest.getInstance("MD5");
        final byte[][] keyAndIv = generateKeyAndIv(AES_KEY_LENGTH, AES_IV_LENGTH, AES_ITERATION, saltData, secret.getBytes(StandardCharsets.UTF_8), md5);
        SecretKeySpec key = new SecretKeySpec(keyAndIv[0], "AES");
        IvParameterSpec iv = new IvParameterSpec(keyAndIv[1]);

        byte[] encrypted = Arrays.copyOfRange(cipherData, 16, cipherData.length);
        Cipher aesCbc = Cipher.getInstance("AES/CBC/PKCS5Padding");
        aesCbc.init(Cipher.DECRYPT_MODE, key, iv);
        byte[] decryptedData = aesCbc.doFinal(encrypted);

        return new String(decryptedData, StandardCharsets.UTF_8);
    }

    public static byte[][] generateKeyAndIv(int keyLength, int ivLength, int iterations, byte[] salt, byte[] password, MessageDigest md) {

        int digestLength = md.getDigestLength();
        int requiredLength = (keyLength + ivLength + digestLength - 1) / digestLength * digestLength;
        byte[] generatedData = new byte[requiredLength];
        int generatedLength = 0;

        try {
            md.reset();

            // Repeat process until sufficient data has been generated
            while (generatedLength < keyLength + ivLength) {

                // Digest data (last digest if available, password data, salt if available)
                if (generatedLength > 0) {
                    md.update(generatedData, generatedLength - digestLength, digestLength);
                }
                md.update(password);
                if (salt != null) {
                    md.update(salt, 0, 8);
                }
                md.digest(generatedData, generatedLength, digestLength);

                // additional rounds
                for (int i = 1; i < iterations; i++) {
                    md.update(generatedData, generatedLength, digestLength);
                    md.digest(generatedData, generatedLength, digestLength);
                }

                generatedLength += digestLength;
            }

            // Copy key and IV into separate byte arrays
            byte[][] result = new byte[2][];
            result[0] = Arrays.copyOfRange(generatedData, 0, keyLength);
            if (ivLength > 0) {
                result[1] = Arrays.copyOfRange(generatedData, keyLength, keyLength + ivLength);
            }

            return result;

        } catch (DigestException e) {
            throw new RuntimeException(e);

        } finally {
            // Clean out temporary data
            Arrays.fill(generatedData, (byte)0);
        }
    }

    public static String getRandomString(int length){
        String s = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-+=_";
        Random random = new Random();
        StringBuilder stringBuffer = new StringBuilder();
        for(int i = 0; i < length; i++){
            int number = random.nextInt(s.length());
            stringBuffer.append(s.charAt(number));
        }
        return stringBuffer.toString();
    }

}
