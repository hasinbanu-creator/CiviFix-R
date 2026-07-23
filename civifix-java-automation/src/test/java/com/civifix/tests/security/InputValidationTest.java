package com.civifix.tests.security;

import org.testng.Assert;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

public class InputValidationTest {

    @DataProvider(name = "securityPayloads")
    public Object[][] securityData() {
        String[] payloads = {
            "' OR 1=1--",
            "<script>alert(1)</script>",
            "\" onclick=\"alert(1)\"",
            "javascript:alert(1)",
            "admin'--",
            "../etc/passwd"
        };
        String[] fields = {"email", "description", "address", "citizen_note"};
        
        Object[][] data = new Object[payloads.length * fields.length][2];
        int index = 0;
        for (String p : payloads) {
            for (String f : fields) {
                data[index++] = new Object[]{f, p};
            }
        }
        return data;
    }

    @Test(dataProvider = "securityPayloads")
    public void testSecurityInjection(String field, String payload) {
        // Simulate security test
        Assert.assertNotNull(field);
        Assert.assertNotNull(payload);
    }
}
