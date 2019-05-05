import javafx.stage.Stage;
import javafx.stage.DirectoryChooser;
import javafx.scene.Scene;
import javafx.fxml.FXML;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.Pane;
import javafx.scene.layout.TilePane;
import javafx.scene.control.*;
import javafx.event.ActionEvent;
import javafx.scene.input.KeyEvent;
import javafx.scene.input.KeyCode;
import javafx.scene.input.MouseEvent;
import javafx.geometry.Insets;
import javafx.concurrent.Task;
import javafx.application.Platform;

import java.io.File;
import java.io.UncheckedIOException;
import java.io.IOException;
import java.io.FileWriter;

import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;


public class Controller {
    private DirectoryChooser folderChooser = new DirectoryChooser();  // Selects a dir
    private FileWriter fileWriter;                                    // Writes to files
    private File directory, sveFileLoc;                               // Path to file or dir
    private File[] fileList;
    private Image pth = new Image(".");                               // Path to image
    private ImageView imgView = new ImageView(pth);                   // Image view area
    private Process pb;                                               // Process runner
    private String tmpPath, resolution, xScreenVal, output, textAreaPth = "",
                   startScrpt = System.getProperty("user.dir") + "/resources/bin/StartXWW.sh";  // Gets shell that starts stuff local
    private int applyType = 1;
    private Stage fileChooserStage;
    @FXML private ListView<?> selXScreenSvr;
    @FXML private Label dirLbl;                                       // Labels
    @FXML private TilePane tilePane;
    @FXML private TextField dirPathField, filePathField;              // Text fields
    @FXML private CheckBox useXSvrn;                                  // Check boxes
    @FXML private ChoiceBox<?> playbackResolution, setMonPosOffset, listSaveLoc;    // Choice box fields
    @FXML private Button applyBttn, closeBttn, fileBttn, clear, killBttn, saveBttn; // Buttons

    @FXML void initialize() throws Exception {
        assert dirPathField != null : "fx:id=\"dirPathField\" was not injected: check your FXML file 'Window.fxml'.";
        assert clear != null : "fx:id=\"clear\" was not injected: check your FXML file 'Window.fxml'.";
        assert filePathField != null : "fx:id=\"filePathField\" was not injected: check your FXML file 'Window.fxml'.";
        assert tilePane != null : "fx:id=\"tilePane\" was not injected: check your FXML file 'Window.fxml'.";
        assert dirLbl != null : "fx:id=\"dirLbl\" was not injected: check your FXML file 'Window.fxml'.";
        assert selXScreenSvr != null : "fx:id=\"selXScreenSvr\" was not injected: check your FXML file 'Window.fxml'.";
        assert closeBttn != null : "fx:id=\"closeBttn\" was not injected: check your FXML file 'Window.fxml'.";
        assert listSaveLoc != null : "fx:id=\"listSaveLoc\" was not injected: check your FXML file 'Window.fxml'.";
        assert setMonPosOffset != null : "fx:id=\"setMonPosOffset\" was not injected: check your FXML file 'Window.fxml'.";
        assert playbackResolution != null : "fx:id=\"playbackResolution\" was not injected: check your FXML file 'Window.fxml'.";
        assert useXSvrn != null : "fx:id=\"useXSvrn\" was not injected: check your FXML file 'Window.fxml'.";
    }

    @FXML void setNewDir(MouseEvent event) { newDir(); }
    @FXML void onEnter(KeyEvent event) {
        if (event.getCode().equals(KeyCode.ENTER)) {
            textAreaPth = dirPathField.getText();
            System.out.println(textAreaPth);
            newDir();
        } else {}
    }

    // Scan selected dir
    public void newDir() {
        tilePane.getChildren().clear();
        Stage stage = new Stage();
        if (textAreaPth != "")
            directory = new File(textAreaPth);
        else {
            directory = folderChooser.showDialog(stage);

            if (directory != null) {
                System.out.println("Directory: " + directory);
            }
        }

        fileList = directory.listFiles();
        dirPathField.setText("" + directory);

        for (int i=0; i<fileList.length; i++) {
            String path = "" + fileList[i];
            if (path.toLowerCase().matches("^.*?(mp4|mpeg|mpg|wmv|mkv|flv|webm|avi|png|jpg|jpeg|gif).*$")) {
                imgView = new ImageView();
 				imgView.setFitWidth(300); // Need these here to get grid properly.
				imgView.setFitHeight(200);
				tilePane.getChildren().add(imgView);
            }
        }

        Task getDir = new Task<Void>() {
            @Override public Void call() {
                newDir2();
                return null;
            }};
        new Thread(getDir).start();
    }
    public void newDir2() {
        for (int i=0; i<fileList.length; i++) {
            String path = "" + fileList[i], tmpP = "" + fileList[i];
            if (tmpP.toLowerCase().matches("^.*?(mp4|mpeg|mpg|wmv|mkv|flv|webm|avi).*$")) {
                String movieImg = "ffmpegthumbnailer -w -t='00:30:00' -c png -i " +
                                         fileList[i] + " -s 300 -o /tmp/image.png",
                       vExec = "mplayer -really-quiet -ao null -loop 0 " + fileList[i];
                try {
                    pb = Runtime.getRuntime().exec(movieImg);
                    pb.waitFor();
                } catch(Throwable imgIOErr) {
                    System.out.println(imgIOErr);
                }

                ImageView view = (ImageView) (tilePane.getChildren().get(i));
                pth = new Image("file:///tmp/image.png");
                Platform.runLater(new Runnable() {
                    @Override public void run() { view.setImage(pth); }
                });

                view.setOnMouseClicked(mouse -> {
					if (mouse.getClickCount() == 2 && !mouse.isConsumed()) {
											            mouse.consume();
						try {
                            pb = Runtime.getRuntime().exec(vExec);
						} catch(IOException vidIOErr) {
							throw new UncheckedIOException(vidIOErr);
						}
					}
                    filePathField.setText(path);
                });
            } else if(tmpP.toLowerCase().matches("^.*?(png|jpg|jpeg|gif).*$")) {
                ImageView view = (ImageView) (tilePane.getChildren().get(i));
			    String title = "file://" + fileList[i];
                pth = new Image(title);

                Platform.runLater(new Runnable() {
                    @Override public void run() { view.setImage(pth); }
                });

				final ImageView imgViewPoped = new ImageView(title);
			    // image click actions
                view.setOnMouseClicked(mouse -> {
					if (mouse.getClickCount() == 2 && !mouse.isConsumed()) {
					    mouse.consume();
    			        displayImg(imgViewPoped, title);
       				}
                    filePathField.setText(path);
			    });
            } else { System.out.println("Not a video or image file."); }
        }
    }
    // Open image in new window
    public void displayImg(ImageView imgViewPoped, String title) {
        Stage popOut = new Stage();
        Pane pane = new Pane();
        imgViewPoped.setLayoutX(0);
        imgViewPoped.setLayoutY(0);
        imgViewPoped.fitWidthProperty().bind(pane.widthProperty());
        imgViewPoped.fitHeightProperty().bind(pane.heightProperty());
        pane.getChildren().add(imgViewPoped);
        Scene scene = new Scene(pane, 1280, 900);
        popOut.setTitle(title);
        popOut.setScene(scene);
        popOut.show();
    }

    @FXML void toggleXscreenUsageField(MouseEvent event) {
        if (useXSvrn.isSelected() == true)
            selXScreenSvr.setDisable(false);
        else if (useXSvrn.isSelected() == false)
            selXScreenSvr.setDisable(true);
    }

    // Kill xwinwrap process
    @FXML void killXWinWrp(ActionEvent event) throws Exception {
        pb = Runtime.getRuntime().exec("killall xwinwrap &");
        pb.waitFor();
    }

    // Pass resolution values
    @FXML void passXScreenVal() {
        xScreenVal = "" + selXScreenSvr.getSelectionModel().getSelectedItem();
    }
    // Preliminary setup to save settings to files
    @FXML void saveToFile(ActionEvent saveEvent) throws Exception {
        // Saves to file with selected and needed settings
        if(filePathField.getText().toLowerCase().matches("^.*?(png|jpg|jpeg|gif).*$"))
            sveFileLoc = new File(System.getProperty("user.home") + "/" + ".config/nitrogen/bg-saved.cfg");
        else
            sveFileLoc = new File(System.getProperty("user.home") + "/" + listSaveLoc.getValue());

        fileWriter = new FileWriter(sveFileLoc);
        resolution = "" + playbackResolution.getValue() + "" + setMonPosOffset.getValue();
        startSave();
    }
    // Save settings to files
    void startSave() throws Exception {
        // XSCREENSAVER
        if (useXSvrn.isSelected() == true) {
            output = "xwinwrap -ov -g " + resolution + " -st -sp -b -nf -s -ni -- /usr/lib/xscreensaver/" + xScreenVal + " -window-id WID -root";
            fileWriter.write(output);
            applyType = 1;
          // GIF
        } else if (filePathField.getText().toLowerCase().contains(".gif")) {
            output = "xwinwrap -ov -g " + resolution + " -st -sp -b -nf -s -ni -- gifview -a -w WID " + filePathField.getText();
            fileWriter.write(output);
            applyType = 1;
        // Standard images using nitrogen
        } else if(filePathField.getText().toLowerCase().contains(".jpg") ||
            filePathField.getText().toLowerCase().contains(".png")) {
            output = "[xin_0] \n file=" + filePathField.getText() + "\nmode=0 \nbgcolor=#000000\n" +
                     "[xin_1] \nfile=" + filePathField.getText() + "\nmode=0 \nbgcolor=#000000";
            fileWriter.write(output);
            applyType = 2;
        //VIDEO
        } else {
            output = "xwinwrap -ov -g " + resolution + " -st -sp -b -nf -s -ni -- mplayer -wid WID -really-quiet -ao null -loop 0 " + filePathField.getText();
            fileWriter.write(output);
            applyType = 1;
        }
    fileWriter.close();
    }

    // Run changes
    @FXML void applySttngs(ActionEvent event) throws Exception {
        pb = Runtime.getRuntime().exec("killall xwinwrap &");
        if (applyType == 1) {
            pb = Runtime.getRuntime().exec(startScrpt);
            pb.waitFor();
        } else if (applyType == 2) {
            pb = Runtime.getRuntime().exec("nitrogen --restore");
            pb.waitFor();
        } else
            pb = Runtime.getRuntime().exec("nitrogen --restore");
            pb.waitFor();
    }
    // Clean selection to start new search.
    @FXML void clearBttnClick(ActionEvent event) {
        tilePane.getChildren().clear();
        tilePane.getChildren().addAll(dirLbl);
        dirPathField.setText("");
        filePathField.setText("");
    }
    // Closes program
    @FXML void closeProg(ActionEvent event) { System.exit(0); }
}
