package com.itdominator.fxwinwrap;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.scene.image.Image;

import java.util.logging.Level;
import java.io.IOException;


public class FXWinWrap extends Application {
    // Classes

    @Override public void start(Stage stage) {
        try {
            FXMLLoader loader = new FXMLLoader(getClass().getResource("resources/FXWinWrap.fxml"));
            loader.setController(new Controller());
            loader.load();
            Scene scene = new Scene(loader.getRoot());
            scene.getStylesheets().add("/com/itdominator/fxwinwrap/resources/stylesheet.css");
            stage.setTitle("FXWinWrap");
            stage.setScene(scene);
        } catch (IOException startException) {
            String message = "\nFXWinWrap Failed to launch...\n";
            System.out.println(message + startException);
        }
        stage.getIcons().add(new Image(FXWinWrap.class.getResourceAsStream("resources/FXWinWrap.png")));
        stage.setResizable(true);
        stage.show();
    }
    public static void main(String[] args) { launch(args); }
}
