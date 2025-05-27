//a java swing application that ask for a name and display hell robert + name

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;  
public class HelloApp extends JFrame {
    private JTextField nameField;
    private JButton greetButton;
    private JLabel greetingLabel;
    public HelloApp() {
        setTitle("Hello App");
        setSize(300, 200);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        nameField = new JTextField(20);
        greetButton = new JButton("Greet");
        greetingLabel = new JLabel("");
        setLayout(new java.awt.FlowLayout());
        add(new JLabel("Enter your name:"));
        add(nameField);
        add(greetButton);
        add(greetingLabel);
        greetButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String name = nameField.getText();
                greetingLabel.setText("Hello, Robert " + name + "!");
            }
        });
    }
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new HelloApp().setVisible(true);


                
            }
        });
    }   
    public void setVisible(boolean b) {
        super.setVisible(b);    
    }
}





