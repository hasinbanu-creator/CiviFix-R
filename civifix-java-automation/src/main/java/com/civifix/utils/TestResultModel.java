package com.civifix.utils;

public class TestResultModel {
    private String testId;
    private String module;
    private String scenario;
    private String errorMsg;
    private String status;
    private String browser;
    private double duration;

    public TestResultModel(String testId, String module, String scenario, String errorMsg, String status, String browser, double duration) {
        this.testId = testId;
        this.module = module;
        this.scenario = scenario;
        this.errorMsg = errorMsg;
        this.status = status;
        this.browser = browser;
        this.duration = duration;
    }

    public String getTestId() { return testId; }
    public String getModule() { return module; }
    public String getScenario() { return scenario; }
    public String getErrorMsg() { return errorMsg; }
    public String getStatus() { return status; }
    public String getBrowser() { return browser; }
    public double getDuration() { return duration; }
}
