package application.pythonInterpret;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.nio.file.Paths;

@Component
public class Interpreter {

    public static final String PATH = "C:\\Users\\khafi\\IdeaProjects\\Bob\\inf_security_main\\";

    @Autowired
    public Interpreter(){}

    public void executeDecryptScript() throws IOException, InterruptedException {
        executeScript("decrypt.py");
        System.out.println("Decryption complete");
    }

    public void executeEncryptScript() throws IOException, InterruptedException {
        executeScript("encrypt.py");
        System.out.println("Encryption complete");
    }

    public void executeInitScript() throws IOException, InterruptedException {
        executeScript("init_decryptor.py");
        System.out.println("Encryption complete");
    }

    public void executeScript(String pathToScript) throws IOException, InterruptedException {
        ProcessBuilder processBuilder = new ProcessBuilder("py", pathToScript);
        processBuilder.redirectErrorStream(true);
        Process process = processBuilder.start();
        process.waitFor();
    }

}
