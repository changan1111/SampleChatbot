package BotAutomationProject.DreamHotelSuite;


import java.io.File;
import java.io.IOException;
import java.util.HashMap;

import org.apache.commons.io.FileUtils;
import org.junit.After;
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
import com.epam.healenium.SelfHealingDriver;

import io.github.bonigarcia.wdm.WebDriverManager;
import junit.framework.Assert;

public class ThirdTest {

	WebDriver driver;

	
	
    private ExtentTest test;
	
	
	@BeforeTest
	public void setup() {
		ExtentReportUtils.initializeExtentReport();

        // Create a new test instance
        test = ExtentReportUtils.createTest("My Test Bangalore");

	}
	
	@Test
	public void DreamHotelTest3() throws IOException {
		WebDriverManager.chromedriver().setup();
		WebDriver delegate = new ChromeDriver();
		driver = SelfHealingDriver.create(delegate);
		test.info("Opening the url");

		driver.get("http://localhost:4200/");
        SPALoadTimeTestListener.startTimer();
        SPALoadTimeTestListener.calculateLoadTime();
		driver.findElement(By.xpath("//input[@ng-reflect-name='text']")).clear();
		driver.findElement(By.xpath("//input[@ng-reflect-name='text']")).sendKeys("Bangalore");
		driver.findElement(By.xpath("//button[text()='Search']")).click();
		test.info("Search value is Bangalore");
		 SPALoadTimeTestListener.startTimer();
	        SPALoadTimeTestListener.calculateLoadTime();		////*[@class='card']/div/div[2]/div[@class='font-superbig']
		String reviewcomment=driver.findElement(By.xpath("//*[@class='card']//div[@class='font-superbig']")).getText();
		test.info(reviewcomment);
		String screenshotPath = FirstTest.takeCaptureScreen(driver); // Capture the screenshot and get its path
	    test.pass("Passed", MediaEntityBuilder.createScreenCaptureFromPath(screenshotPath).build());
		
		Assert.assertEquals("3.7", reviewcomment);
		takecaptureScreen(driver);
		driver.findElement(By.xpath("//input[@ng-reflect-name='text']")).clear();
		driver.findElement(By.xpath("//input[@ng-reflect-name='text']")).sendKeys("Bangalore");
		driver.findElement(By.xpath("//*[text()='Search']")).click();
		SPALoadTimeTestListener.startTimer();
	    SPALoadTimeTestListener.calculateLoadTime();
		test.info("End of DreamHotel Test3");


	}
	
	
	
	public static void takecaptureScreen(WebDriver driver) throws IOException {
		driver=((SelfHealingDriver)driver).getDelegate();		
		TakesScreenshot screen = ((TakesScreenshot) driver);
		File src = screen.getScreenshotAs(OutputType.FILE);
		String dest =  System.getProperty("user.dir")+ "\\"+ System.currentTimeMillis() + ".png";
		System.out.println(dest);
		File target = new File(dest);
		FileUtils.copyFile(src, target);
		//return target.getAbsolutePath();
		}
	
	
	 @AfterTest
	    public void finalizeReport() {
		 HashMap<String, String> ExtentLogs = ExtentReportUtils.extractLogs(test.getModel().getLogs());
		  System.out.println(ExtentLogs.get("LogDetails"));
	        // Flush the Extent Report after all test cases finish
		 ExtentReportUtils.flushReport();
		 driver.close();
	    	//ExtentReportUtils.removeTest();
	    }
	
}
