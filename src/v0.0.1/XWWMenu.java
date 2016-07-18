import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.scene.layout.AnchorPane;


public class XWWMenu extends Application {
    @Override
    public void start(Stage stage) throws Exception {
        Scene scene = new Scene(FXMLLoader.load(XWWMenu.class.getResource("resources/Window.fxml")));
        stage.setScene(scene);
        stage.setTitle("XWinWrap Menu");
        stage.setResizable(false);
        stage.show();
    }
    public static void main(String[] args) { launch(args); }
}
