package BotAutomationProject.DreamHotelSuite;
import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.model.Log;
import com.aventstack.extentreports.reporter.ExtentSparkReporter;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.List;

public class ExtentReportUtils {
    private static ExtentReports extent;
    private static ThreadLocal<ExtentTest> extentTest = new ThreadLocal<>();
    private static String reportPath;

    public static void initializeExtentReport() {
        if (reportPath == null) {
            String timestamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
            String projectDir = System.getProperty("user.dir");
            reportPath = projectDir + File.separator + "extent_report_" + timestamp + ".html";
            ExtentSparkReporter htmlReporter = new ExtentSparkReporter(reportPath);
            extent = new ExtentReports();
            extent.attachReporter(htmlReporter);
            System.out.println(reportPath);
        }
    }

    public static ExtentTest createTest(String testName) {
        ExtentTest test = extent.createTest(testName);
        extentTest.set(test);
        return test;
    }

    public static ExtentTest getCurrentTest() {
        return extentTest.get();
    }
    
    public static void removeTest() {
        extentTest.remove();
    }

    public static void flushReport() {
        extent.flush();
    }
    
    
    public static HashMap<String,String> extractLogs(List<Log> blabla) {
    	String steps=null;
    	int statusCode=1;
    	
    	HashMap<String,String> results=new HashMap<>();
    	
    	for(int i=0;i<=blabla.size()-1;i++) {
    		if(steps==null) {
    			steps = blabla.get(i).getStatus().toString().toUpperCase() + " "
    					+blabla.get(i).getTimestamp().toString().toUpperCase() + " "+
    					blabla.get(i).getDetails().toString().toUpperCase() +"\n";
    		}else {
    			steps = steps + blabla.get(i).getStatus().toString().toUpperCase() + " "
    					+blabla.get(i).getTimestamp().toString().toUpperCase() + " "+
    					blabla.get(i).getDetails().toString().toUpperCase() +"\n";	
    		}
    		
    		if(blabla.get(i).getStatus().toString().toUpperCase()=="Failed") {
    			statusCode=5;
    		}
    		
    	}
    	results.put("StatusCode", Integer.toString(statusCode));
    	results.put("LogDetails", steps);
    	return results;
    }
}
