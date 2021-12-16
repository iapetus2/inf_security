package application.services;

import application.http.HttpGenerator;
import application.managers.MainManager;
import application.pythonInterpret.Interpreter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.FileOutputStream;
import java.io.OutputStream;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

@Component
public class MainService {

    public Interpreter interpreter;
    public MainManager mainManager;
    public HttpGenerator httpGenerator;
    public Executor executor;

    private static final String PATH = "C:\\Users\\khafi\\IdeaProjects\\Bob\\inf_security_main\\data\\keys\\";

    @Autowired
    public MainService(Interpreter interpreter, MainManager mainManager, HttpGenerator httpGenerator, Executor executor) {
        this.interpreter = interpreter;
        this.mainManager = mainManager;
        this.httpGenerator = httpGenerator;
        ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
        scheduler.scheduleAtFixedRate(executor, 2, 2, TimeUnit.SECONDS);
    }

    public String receivedFriendOpenKey(String inputFile) throws Exception {

        if (mainManager.pathAsString(mainManager.openKey).length() == 0) {
            Path originalPath = Paths.get(PATH + "another_public_key.txt");
            OutputStream file = new FileOutputStream(originalPath.toFile());
            file.write(inputFile.getBytes());
            file.close();
            mainManager.receivedKey = originalPath;
            interpreter.executeInitScript();
            mainManager.receivedKey = originalPath;
            mainManager.openKey = Paths.get(PATH + "my_public_key.txt");
            mainManager.secretKey = Paths.get(PATH + "my_secret_key.txt");

            httpGenerator.executePost("http://localhost:8081/", mainManager.pathAsString(mainManager.openKey));

            return mainManager.pathAsString(mainManager.openKey);
        } else {
            return null;
        }
    }

    public void receivedMessage(String inputFile) throws Exception {
        Path originalPath = Paths.get("/data/decr/input.txt");
        OutputStream file = new FileOutputStream(originalPath.toFile());
        file.write(inputFile.getBytes());
        file.close();
        if (mainManager.pathAsString(mainManager.openKey).length() != 0) {
            interpreter.executeDecryptScript();
        }
    }
}
