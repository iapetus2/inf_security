package application.controllers;

import application.http.HttpGenerator;
import application.services.MainService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MainController {

    @Autowired
    private MainService mainService;

    public String response;

    @PostMapping("/openKey")
    public ResponseEntity<?> getOpenKey(@RequestBody String inputFile) throws Exception {
        response = mainService.receivedFriendOpenKey(inputFile);
        if (response != null) {

            return new ResponseEntity<>(response, HttpStatus.OK);
        } else {
            return new ResponseEntity<>(HttpStatus.OK);
        }
    }

    @PostMapping("/message")
    public ResponseEntity<?> sendMessage(@RequestBody String inputFile) throws Exception {
        mainService.receivedMessage(inputFile);

        return new ResponseEntity<>(HttpStatus.OK);
    }

}

