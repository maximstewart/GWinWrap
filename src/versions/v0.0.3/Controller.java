import javafx.stage.*;
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
import java.io.*;


public class Controller {
	 		private DirectoryChooser folderChooser = new DirectoryChooser();  // Selects a dir
  		private FileChooser fileChooser = new FileChooser();  // Selects a file
 			private FileWriter fileWriter;  // Writes to files
    private File directory, sveFileLoc;  // Path to file or dir
    private Image pth = new Image(".");  // Path to image
    private ImageView imgView = new ImageView(pth);  // Image view area
    private Process pb;  // Process runner
    private String tmpPath, resolution, xScreenVal, output,
                   startScrpt = System.getProperty("user.dir") + "/resources/bin/StartXWW.sh",  // Gets shell that starts stuff local
                   textAreaPth = "";
    private int applyType = 1;
    private Stage fileChooserStage;
    @FXML private ListView<?> selXScreenSvr;
    @FXML private Label dirLbl, errorField;  // Labels
    @FXML private TilePane tilePane;
    @FXML private TextField dirPathField, filePathField;  // Text fields
    @FXML private CheckBox lftScrn, rghtScrn, useXSvrn;  // Check boxes
    @FXML private ChoiceBox<?> listLftRes, listRgthRes, listSaveLoc; // Choice box fields
    @FXML private Button applyBttn, closeBttn, fileBttn, clear, // Buttons
                         killBttn, restartBttn, saveBttn;

    // This method is called by the FXMLLoader when initialization is complete
    @FXML void initialize() throws Exception {
        assert clear != null : "fx:id=\"clear\" was not injected: check your FXML file 'Window.fxml'.";
        assert closeBttn != null : "fx:id=\"closeBttn\" was not injected: check your FXML file 'Window.fxml'.";
        assert dirLbl != null : "fx:id=\"dirLbl\" was not injected: check your FXML file 'Window.fxml'.";
        assert errorField != null : "fx:id=\"errorField\" was not injected: check your FXML file 'Window.fxml'.";
        assert filePathField != null : "fx:id=\"filePathField\" was not injected: check your FXML file 'Window.fxml'.";
        assert lftScrn != null : "fx:id=\"lftScrn\" was not injected: check your FXML file 'Window.fxml'.";
        assert listLftRes != null : "fx:id=\"listLftRes\" was not injected: check your FXML file 'Window.fxml'.";
        assert listRgthRes != null : "fx:id=\"listRgthRes\" was not injected: check your FXML file 'Window.fxml'.";
        assert listSaveLoc != null : "fx:id=\"listSaveLoc\" was not injected: check your FXML file 'Window.fxml'.";
        assert rghtScrn != null : "fx:id=\"rghtScrn\" was not injected: check your FXML file 'Window.fxml'.";
        assert selXScreenSvr != null : "fx:id=\"selXScreenSvr\" was not injected: check your FXML file 'Window.fxml'.";
        assert tilePane != null : "fx:id=\"tilePane\" was not injected: check your FXML file 'Window.fxml'.";
        assert useXSvrn != null : "fx:id=\"useXSvrn\" was not injected: check your FXML file 'Window.fxml'.";
        // Initialize your logic here: all @FXML variables will have been injected

        ffmpegChker();
    }

    // Handler for TextArea[fx:id="dirPathField"] onKeyReleased
    @FXML void setNewDir(MouseEvent event) { newDir(); }
    @FXML void onEnter(KeyEvent event) {
        if (event.getCode().equals(KeyCode.ENTER)) {
            textAreaPth = dirPathField.getText();
            System.out.println(textAreaPth);
            newDir();
        }
        else
             System.out.println("Not calling newDir...");
    }

    // Scan selected dir
    public void newDir() {
        Stage stage = new Stage();
        if (textAreaPth != "")
            directory = new File(textAreaPth);
        else
            directory = folderChooser.showDialog(stage);

        File[] fileList = directory.listFiles();
        int size = fileList.length;
        tilePane.getChildren().clear();
        dirPathField.setText("" + directory);
			     for (int i=0; i<size; i++) {
            String path = "" + fileList[i];
            if (fileList[i].getName().contains(".mp4") || fileList[i].getName().contains(".mpeg") ||
                fileList[i].getName().contains(".mpg") || fileList[i].getName().contains(".wmv") ||
                fileList[i].getName().contains(".mkv") || fileList[i].getName().contains(".flv") ||
                fileList[i].getName().contains(".webm") || fileList[i].getName().contains(".avi")) {
                    String movieImg = "ffmpegthumbnailer -w -t='00:30:00' -c png -i " + fileList[i] +
                                                                " -s 300 -o /tmp/image.png",
                           vExec = "mplayer " + fileList[i];
                    try {
                        pb = Runtime.getRuntime().exec(movieImg);
                        pb.waitFor();
                            System.out.println(movieImg);
                    } catch(Throwable imgIOErr) {
                            System.out.println(imgIOErr);
                    }
        												imgView =  new ImageView("file:///tmp/image.png");
 					              imgView.setFitWidth(300); // Need these here to get grid properly.
						              imgView.setFitHeight(200);
					 		        				tilePane.getChildren().add(imgView);
                    imgView.setOnMouseClicked(mouse -> {
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
            } else if(fileList[i].getName().contains(".png") || fileList[i].getName().contains(".jpg")||
                      fileList[i].getName().contains(".gif") || fileList[i].getName().contains(".jpeg")) {
												              imgView =  new ImageView("file://" + fileList[i]);
			                       String title = "" + fileList[i];
												              imgView.setFitWidth(300); // Need these here to get grid properly.
												              imgView.setFitHeight(200);
								 			              tilePane.getChildren().add(imgView);
												              final ImageView imgViewPoped =  new ImageView("file://" + fileList[i]);
			                       // image click actions
			                       imgView.setOnMouseClicked(mouse -> {
								                      if (mouse.getClickCount() == 2 && !mouse.isConsumed()) {
								                          mouse.consume();
    			                           displayImg(imgViewPoped, title);
       								               }
                          filePathField.setText(path);
			                       });
								    } else {
                   System.out.println("Not a video or image file.");
            }
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

    // Kill xwinwrap process
    @FXML void killXWinWrp(ActionEvent event) throws Exception {
        pb = Runtime.getRuntime().exec("killall xwinwrap &");
        pb.waitFor();
    }
    // Restart xwinwrap process
    @FXML void restartXWinWrp(ActionEvent event) throws Exception {
        pb = Runtime.getRuntime().exec("killall xwinwrap &");
        pb = Runtime.getRuntime().exec(startScrpt);
        pb.waitFor();
    }
    // Pass resolution values
    @FXML void passXScreenVal() {
        xScreenVal = "" + selXScreenSvr.getSelectionModel().getSelectedItem();
    }
    // Preliminary setup to save settings to files
    @FXML void saveToFile(ActionEvent saveEvent) throws Exception {

        // Saves to file with selected and needed settings
        if(filePathField.getText().toLowerCase().contains(".jpg") ||
           filePathField.getText().toLowerCase().contains(".jpeg") ||
           filePathField.getText().toLowerCase().contains(".png") ||
           filePathField.getText().toLowerCase().contains(".gif"))
              sveFileLoc = new File(System.getProperty("user.home") + "/" + ".config/nitrogen/bg-saved.cfg");
        else
              sveFileLoc = new File(System.getProperty("user.home") + "/" + listSaveLoc.getValue());

        fileWriter = new FileWriter(sveFileLoc);
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
                output = "xwinwrap -ov -g " + resolution + " -st -sp -b -nf -s -ni -- mplayer -wid WID -really-quiet -nosound -loop 0 " + filePathField.getText();
                fileWriter.write(output);
                applyType = 1;
        }
    fileWriter.close();
    }

    void ffmpegChker() throws Exception {
            File ffmpgLoc = new File("/usr/bin/ffmpegthumbnailer");
            boolean exists = ffmpgLoc.exists();
            System.out.println("" + exists);
            if (exists) {
               System.out.println("Ffmpeg is present....");
             } else {
               String installer = System.getProperty("user.dir") + "/resources/bin/InstallFFMPEGTHUMB.sh";
															pb = Runtime.getRuntime().exec(installer);
															pb.waitFor();
            }
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
