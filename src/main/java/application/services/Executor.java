package application.services;

import application.managers.MainManager;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.*;
import java.nio.file.Paths;

@Component
public class Executor implements Runnable {

    public MainManager mainManager;

    @Autowired
    public Executor(MainManager mainManager){
        this.mainManager = mainManager;
    }

    @Override
    public void run() {
        try {
            InputStream inputStream = new FileInputStream(mainManager.message.toFile());
            if (inputStream.readAllBytes().length != 0) {
                inputStream.close();
                mainManager.manage();
            }
            inputStream.close();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
