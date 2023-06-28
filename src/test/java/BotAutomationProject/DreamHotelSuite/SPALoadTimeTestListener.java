package BotAutomationProject.DreamHotelSuite;

import org.junit.jupiter.api.extension.AfterTestExecutionCallback;
import org.junit.jupiter.api.extension.ExtensionContext;

public class SPALoadTimeTestListener implements AfterTestExecutionCallback {

    private static ThreadLocal<Double> startTime = new ThreadLocal<>();

    @Override
    public void afterTestExecution(ExtensionContext context) {
        double loadTime = calculateLoadTime();
        System.out.println("Page Load Time: " + loadTime + " milliseconds");
    }

    public static double calculateLoadTime() {
        double endTime = System.currentTimeMillis();
        double startTimeValue = startTime.get();
        startTime.remove();
        double loadTime=endTime - startTimeValue;
        System.out.println(loadTime);
        return loadTime;
    }

    public static void startTimer() {
        startTime.set((double) System.currentTimeMillis());
    }
}
