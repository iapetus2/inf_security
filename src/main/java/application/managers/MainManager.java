package application.managers;

import application.http.HttpGenerator;
import application.pythonInterpret.Interpreter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.PostMapping;

import javax.annotation.PostConstruct;
import javax.persistence.criteria.CriteriaBuilder;
import java.io.*;
import java.nio.file.Path;
import java.nio.file.Paths;

@Component
public class MainManager {

    private static final String PATH = "C:\\Users\\khafi\\IdeaProjects\\Bob\\inf_security_main\\data\\";

    public Interpreter interpreter;
    public HttpGenerator httpGenerator;
    public Path openKey = null;
    public Path message;
    public Path encryptedMessage;
    public Path secretKey = null;
    public Path receivedKey;
    public Path receivedMessage;

    @Autowired
    public MainManager(Interpreter interpreter, HttpGenerator httpGenerator) throws IOException {
        this.interpreter = interpreter;
        this.httpGenerator = httpGenerator;
    }

    @PostConstruct
    public void init() throws IOException {
        this.openKey = createPath("keys/my_public_key.txt");
        this.message = createPath("encr/input.txt");
        this.encryptedMessage = createPath("encr/output.txt");
        this.secretKey = createPath("keys/my_private_key.txt");
        this.receivedKey = createPath("keys/another_public_key.txt");
        this.receivedMessage = createPath("decr/input.txt");
    }


    public void manage() throws IOException, InterruptedException {
         if (openKey == null || pathAsString(openKey).length() == 1) {
            interpreter.executeInitScript();
            openKey = Paths.get(PATH + "keys/my_public_key.txt");
            secretKey = Paths.get(PATH + "keys/my_private_key.txt");
            String response = httpGenerator.executePost("http://localhost:8081/openKey", pathAsString(openKey));
            Path originalPath = Paths.get(PATH + "keys/another_public_key.txt");
            OutputStream file = new FileOutputStream(originalPath.toFile());
             if (response != null) {
                 file.write(response.getBytes());
             }
            file.close();
            receivedKey = originalPath;
            
            return;
        }
        interpreter.executeEncryptScript();
        encryptedMessage = Paths.get(PATH + "/encr/output.txt");
        httpGenerator.executePost("http://localhost:8081/message", pathAsString(encryptedMessage));
        message = createPath(PATH + "decr/input.txt");
    }

    public String pathAsString(Path path) throws IOException {
        InputStream stream = new FileInputStream(path.toFile());
        String result = new String(stream.readAllBytes());
        stream.close();

        return result;
    }

    public Path createPath(String pathname) throws IOException {
        Path path = Paths.get(PATH + pathname);
        path.toFile().delete();
        OutputStream file = new FileOutputStream(path.toFile());
        file.close();

        return path;
    }
}
