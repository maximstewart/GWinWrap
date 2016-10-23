import javafx.stage.Stage;
import javafx.fxml.FXML;
import javafx.stage.FileChooser;
import javafx.scene.Scene;
import javafx.scene.layout.Pane;
import javafx.scene.layout.AnchorPane;
import javafx.scene.image.ImageView;
import javafx.scene.image.Image;
import javafx.scene.media.Media;
import javafx.scene.media.MediaView;
import javafx.scene.media.MediaPlayer;
import javafx.scene.control.*;
import javafx.event.ActionEvent;
import java.io.*;


public class Controller {
  		private FileChooser fileChooser = new FileChooser();
    private String tmpPath, resolution, xScreenVal, output,
                   startScrpt = System.getProperty("user.dir") + "/resources/bin/StartXWW.sh",
                   ffmpg = System.getProperty("user.dir") + "/resources/bin/ffmpegthumbnailer";
    private int applyType = 1;
    private Stage fileChooserStage;
    private Image imgPath;
    private Process pb;
    private File file;
 			private FileWriter fileWriter;
    @FXML private AnchorPane imgVideoField;
    @FXML private ImageView imgView;
    @FXML private ListView<?> selXScreenSvr;
    @FXML private TextField txtField;
    @FXML private Label errorField;
    @FXML private CheckBox lftScrn, rghtScrn, useXSvrn;
    @FXML private ChoiceBox<?> listLftRes, listRgthRes, listSaveLoc;
    @FXML private Button applyBttn, closeBttn, dirBttn,
                         killBttn, restartBttn, saveBttn;
    @FXML
    void closeProg(ActionEvent event) {
        System.exit(0);
    }
    @FXML
    void getImg(ActionEvent event) throws Exception {
        fileChooser.setTitle("Open Image File");
        tmpPath = "" + fileChooser.showOpenDialog(fileChooserStage);
        txtField.setText(tmpPath);
        if (txtField.getText().toLowerCase().contains(".mp4") ||
            txtField.getText().toLowerCase().contains(".mkv") ||
            txtField.getText().toLowerCase().contains(".mpg") ||
            txtField.getText().toLowerCase().contains(".mpeg") ||
            txtField.getText().toLowerCase().contains(".wmv") ||
            txtField.getText().toLowerCase().contains(".flv") ||
            txtField.getText().toLowerCase().contains(".webm") ||
            txtField.getText().toLowerCase().contains(".avi")) {
        /*    ##########  FOR FUTURE PLAYING VIDEO  ##########
          pb = new ProcessBuilder("mplayer", "-slave", "-quiet", "-idle", tmpPath).start();
          Media media = new Media(getClass().getResource("test.mp4").toString());
          // Create the player and set to play automatically.
          final MediaPlayer mediaPlayer = new MediaPlayer(media);
          mediaPlayer.setAutoPlay(true);
          final MediaView mediaView = new MediaView(mediaPlayer);
          imgVideoField.getChildren().clear();
          imgVideoField.getChildren().addAll(mediaView);
        */
            String movieImg = ffmpg + " -w -t='00:10:00' -c jpg -i " + tmpPath +
                                                    " -s 800 -o /tmp/image.jpg";
            pb = Runtime.getRuntime().exec(movieImg);
            pb.waitFor();
            imgPath = new Image("file://" + "/tmp/image.jpg");
            tmpPath = "/tmp/image.jpg";
        }
        else {
            imgPath = new Image("file://" + tmpPath);
        }

 							imgView.setFitWidth(500);
								imgView.setFitHeight(375);
        imgView.setImage(imgPath);
        String title = "" + tmpPath;
								final ImageView imgViewPoped = new ImageView("file://" + tmpPath);
        setClick(imgViewPoped, title);

        if(txtField.getText().toLowerCase().contains(".jpg") ||
           txtField.getText().toLowerCase().contains(".png"))
           applyType = 2;
    }
    void setClick(ImageView imgViewPoped, String title) {
        imgView.setOnMouseClicked(e -> {
            imgViewPoped.setLayoutX(0);
            imgViewPoped.setLayoutY(0);
            Stage popOut = new Stage();
            Pane pane = new Pane();
            imgViewPoped.fitWidthProperty().bind(pane.widthProperty());
            imgViewPoped.fitHeightProperty().bind(pane.heightProperty());
            pane.getChildren().addAll(imgViewPoped);
            Scene scene = new Scene(pane, 800, 600);
            popOut.setTitle(title);
            popOut.setScene(scene);
            popOut.show();
        });
    }
    @FXML
    void killXWinWrp(ActionEvent event) throws Exception {
        pb = Runtime.getRuntime().exec("killall xwinwrap &");
    }
    @FXML
    void restartXWinWrp(ActionEvent event) throws Exception {
        pb = Runtime.getRuntime().exec("killall xwinwrap &");
        pb = Runtime.getRuntime().exec(startScrpt);
    }
    @FXML
    void passXScreenVal() {
        xScreenVal = "" + selXScreenSvr.getSelectionModel().getSelectedItem();
    }
    @FXML
    void saveToFile(ActionEvent event) throws Exception {
        // Saves to file with selected and needed settings
        if(txtField.getText().toLowerCase().contains(".jpg") ||
           txtField.getText().toLowerCase().contains(".png"))
              file = new File(System.getProperty("user.home") + "/" + ".config/nitrogen/bg-saved.cfg");
        else
              file = new File(System.getProperty("user.home") + "/" + listSaveLoc.getValue());
        fileWriter = new FileWriter(file);

        errorField.setText("");
        if (lftScrn.isSelected() == true && rghtScrn.isSelected() == true)
              errorField.setText("Please only check one...");
        else if (lftScrn.isSelected() == false && rghtScrn.isSelected() == false)
              errorField.setText("Please check one...");
        else if (lftScrn.isSelected() == true && rghtScrn.isSelected() == false) {
            resolution = "" + listLftRes.getValue();
            startSave();
        }
        else if (rghtScrn.isSelected() == true && lftScrn.isSelected() == false) {
                resolution = "" + listLftRes.getValue() + "" + listRgthRes.getValue();
                startSave();
        } else { startSave(); }
    }
    void startSave() throws Exception {
        // XSCREENSAVER
        if (useXSvrn.isSelected() == true) {
            output = "xwinwrap -ov -g " + resolution + " -st -sp -b -nf -s -ni -- /usr/lib/xscreensaver/" + xScreenVal + " -window-id WID -root";
            fileWriter.write(output);
            applyType = 1;
          // GIF
        } else if (txtField.getText().toLowerCase().contains(".gif")) {
                output = "xwinwrap -ov -g " + resolution + " -st -sp -b -nf -s -ni -- gifview -a -w WID " + txtField.getText();
                fileWriter.write(output);
                applyType = 1;
          // Standard images using nitrogen
        } else if(txtField.getText().toLowerCase().contains(".jpg") ||
                txtField.getText().toLowerCase().contains(".png")) {
                output = "[xin_0] \n file=" + txtField.getText() + "\nmode=0 \nbgcolor=#000000\n" +
                         "[xin_1] \nfile=" + txtField.getText() + "\nmode=0 \nbgcolor=#000000";
                fileWriter.write(output);
                applyType = 2;
          //VIDEO
        } else {
                output = "xwinwrap -ov -g " + resolution + " -st -sp -b -nf -s -ni -- mplayer -wid WID -nosound -loop 0 " + txtField.getText();
                fileWriter.write(output);
                applyType = 1;
        }
    fileWriter.close();
    }
    @FXML
    void applySttngs(ActionEvent event) throws Exception {
        pb = Runtime.getRuntime().exec("killall xwinwrap &");
        if (applyType == 1) {
            pb = Runtime.getRuntime().exec(startScrpt);
        } else if (applyType == 2) {
            pb = Runtime.getRuntime().exec("nitrogen --restore");
        } else
            pb = Runtime.getRuntime().exec("nitrogen --restore");
    }
    @FXML
    void initialize() {
        assert applyBttn != null : "fx:id=\"applyBttn\" was not injected: check your FXML file 'Window.fxml'.";
        assert closeBttn != null : "fx:id=\"closeBttn\" was not injected: check your FXML file 'Window.fxml'.";
        assert dirBttn != null : "fx:id=\"dirBttn\" was not injected: check your FXML file 'Window.fxml'.";
        assert errorField != null : "fx:id=\"errorField\" was not injected: check your FXML file 'Window.fxml'.";
        assert imgVideoField != null : "fx:id=\"imgVideoField\" was not injected: check your FXML file 'Window.fxml'.";
        assert imgView != null : "fx:id=\"imgView\" was not injected: check your FXML file 'Window.fxml'.";
        assert killBttn != null : "fx:id=\"killBttn\" was not injected: check your FXML file 'Window.fxml'.";
        assert lftScrn != null : "fx:id=\"lftScrn\" was not injected: check your FXML file 'Window.fxml'.";
        assert listLftRes != null : "fx:id=\"listLftRes\" was not injected: check your FXML file 'Window.fxml'.";
        assert listRgthRes != null : "fx:id=\"listRgthRes\" was not injected: check your FXML file 'Window.fxml'.";
        assert listSaveLoc != null : "fx:id=\"listSaveLoc\" was not injected: check your FXML file 'Window.fxml'.";
        assert restartBttn != null : "fx:id=\"restartBttn\" was not injected: check your FXML file 'Window.fxml'.";
        assert rghtScrn != null : "fx:id=\"rghtScrn\" was not injected: check your FXML file 'Window.fxml'.";
        assert saveBttn != null : "fx:id=\"saveBttn\" was not injected: check your FXML file 'Window.fxml'.";
        assert selXScreenSvr != null : "fx:id=\"selXScreenSvr\" was not injected: check your FXML file 'Window.fxml'.";
        assert txtField != null : "fx:id=\"txtField\" was not injected: check your FXML file 'Window.fxml'.";
        assert useXSvrn != null : "fx:id=\"useXSvrn\" was not injected: check your FXML file 'Window.fxml'.";
    }
}
