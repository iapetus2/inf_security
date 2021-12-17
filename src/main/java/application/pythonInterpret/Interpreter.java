package application.pythonInterpret;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class Interpreter {

    public static final String PATH = "C:\\Users\\khafi\\IdeaProjects\\Bob\\inf_security_main\\src\\main\\java\\application\\python\\";

    @Autowired
    public Interpreter(){}

    public void executeDecryptScript() throws IOException, InterruptedException {
        executeScript(PATH + "decrypt.py");
        System.out.println("Decryption complete");
    }

    public void executeEncryptScript() throws IOException, InterruptedException {
        executeScript(PATH + "encrypt.py");
        System.out.println("Encryption complete");
    }

    public void executeInitScript() throws IOException, InterruptedException {
        System.out.println("C:\\Users\\khafi\\IdeaProjects\\Bob\\inf_security_main\\src\\main\\java\\application\\python\\init_decryptor.py");
        executeScript(PATH + "init_decryptor.py");
        System.out.println("Initialization complete");
    }

    public void executeScript(String pathToScript) throws IOException, InterruptedException {
        ProcessBuilder processBuilder = new ProcessBuilder("py", "C:\\Users\\khafi\\IdeaProjects\\Bob\\inf_security_main\\src\\main\\java\\application\\python\\init_decryptor.py");
        processBuilder.redirectErrorStream(true);
        Process process = processBuilder.start();
        process.waitFor();
        process.destroy();
    }

}
