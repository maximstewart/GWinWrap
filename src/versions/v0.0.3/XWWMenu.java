import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.scene.layout.AnchorPane;



public class XWWMenu extends Application {
    @Override
    public void start(final Stage stage) throws Exception {
        Scene scene = new Scene(FXMLLoader.load(XWWMenu.class.getResource("resources/Window.fxml")));
        scene.getStylesheets().add("resources/stylesheet.css");
        stage.setScene(scene);
        //stage.setResizable(false);  // keeps window from resizing
        stage.setTitle("XWinWrap Menu");
        stage.setMinWidth(800);
        stage.setMinHeight(600);
        stage.show();
    }
    // needed because you know... it's java.
    public static void main(String[] args) { launch(args); }
}
