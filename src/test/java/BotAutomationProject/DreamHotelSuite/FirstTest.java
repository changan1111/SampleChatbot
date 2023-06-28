package BotAutomationProject.DreamHotelSuite;


import java.io.File;
import java.io.IOException;
import java.util.HashMap;

import org.apache.commons.io.FileUtils;
import org.openqa.selenium.By;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.annotations.AfterTest;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Test;

import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.MediaEntityBuilder;
import com.aventstack.extentreports.model.Media;
import com.epam.healenium.SelfHealingDriver;

import io.github.bonigarcia.wdm.WebDriverManager;
import junit.framework.Assert;

public class FirstTest {

	WebDriver driver;
	
	
    private ExtentTest test;
	
	
	@BeforeTest
	public void setup() {
		ExtentReportUtils.initializeExtentReport();

        // Create a new test instance
        test = ExtentReportUtils.createTest("My Test Chennai");
       

	}
	

	@Test
	public void DreamHotelTest1() throws IOException {
		WebDriverManager.chromedriver().setup();
		WebDriver delegate = new ChromeDriver();
		driver = SelfHealingDriver.create(delegate);
		test.info("Opening the url");
		driver.get("http://localhost:4200/");
        SPALoadTimeTestListener.startTimer();
        SPALoadTimeTestListener.calculateLoadTime();
		driver.findElement(By.xpath("//input[@ng-reflect-name='text']")).clear();
		driver.findElement(By.xpath("//input[@ng-reflect-name='text']")).sendKeys("Chennai");
		driver.findElement(By.xpath("//button[text()='Search']")).click();
		test.info("Search value is Chennai");
		SPALoadTimeTestListener.startTimer();
	    SPALoadTimeTestListener.calculateLoadTime();		////*[@class='card']/div/div[2]/div[@class='font-superbig']
		String reviewcomment=driver.findElement(By.xpath("//*[@class='card']//div[@class='font-superbig']")).getText();
	    String screenshotPath = takeCaptureScreen(driver); // Capture the screenshot and get its path
	    //test.pass("Passed", MediaEntityBuilder.createScreenCaptureFromPath(screenshotPath).build());
		test.info("review comment is: "+reviewcomment);
	    Assert.assertEquals("3.1", reviewcomment);
		takeCaptureScreen(driver);
		driver.findElement(By.xpath("//input[@ng-reflect-name='text']")).clear();
		driver.findElement(By.xpath("//input[@ng-reflect-name='text']")).sendKeys("Chennai");
		driver.findElement(By.xpath("//*[text()='Search']")).click();
		SPALoadTimeTestListener.startTimer();
	    SPALoadTimeTestListener.calculateLoadTime();
		test.info("End of Dream Hotel Test1");

	}
	
	
	
	public static String takeCaptureScreen(WebDriver driver) throws IOException {
	    driver = ((SelfHealingDriver) driver).getDelegate();
	    TakesScreenshot screen = ((TakesScreenshot) driver);
	    File src = screen.getScreenshotAs(OutputType.FILE);
	    String dest = System.getProperty("user.dir") + "\\"
	            + System.currentTimeMillis() + ".png";
	    System.out.println(dest);
	    File target = new File(dest);
	    FileUtils.copyFile(src, target);
	    return dest; // Return the path of the captured screenshot
	}
	
	
	  @AfterTest
	    public void finalizeReport() {
	        // Flush the Extent Report after all test cases finish
		  System.out.println(test.getModel().getLogs());
		  HashMap<String, String> ExtentLogs = ExtentReportUtils.extractLogs(test.getModel().getLogs());
		  
		  System.out.println(ExtentLogs.get("LogDetails"));
		  ExtentReportUtils.flushReport();
		  driver.close();
		 // ExtentReportUtils.removeTest();
	       
	    }
	
}
