package gui;

import parser.*;

import javax.swing.*;
import javax.swing.tree.DefaultMutableTreeNode;
import java.awt.*;
import java.awt.datatransfer.DataFlavor;
import java.awt.dnd.*;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.List;
import java.util.Map;

public class JsonParserGUI extends JFrame {

    private JTextArea inputArea;
    private JTree jsonTree;
    private JLabel statusLabel;

    public JsonParserGUI() {
        setTitle("JSON Parser");
        setSize(800, 600);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout());

        // Menu bar
        JMenuBar menuBar = new JMenuBar();
        JMenu fileMenu = new JMenu("File");
        JMenuItem openItem = new JMenuItem("Open JSON File...");
        openItem.addActionListener(e -> openJsonFile());
        fileMenu.add(openItem);
        menuBar.add(fileMenu);
        setJMenuBar(menuBar);

        // Input area
        inputArea = new JTextArea();
        JScrollPane inputScroll = new JScrollPane(inputArea);
        inputScroll.setBorder(BorderFactory.createTitledBorder("JSON Input"));

        // Drag-and-drop support
        new DropTarget(inputArea, new DropTargetAdapter() {
            @SuppressWarnings("unchecked")
            @Override
            public void drop(DropTargetDropEvent dtde) {
                try {
                    dtde.acceptDrop(DnDConstants.ACTION_COPY);
                    List<File> droppedFiles = (List<File>)
                            dtde.getTransferable().getTransferData(DataFlavor.javaFileListFlavor);
                    if (!droppedFiles.isEmpty()) {
                        File file = droppedFiles.get(0);
                        loadJsonFromFile(file);
                    }
                } catch (Exception ex) {
                    showError("Drag-and-drop failed: " + ex.getMessage());
                }
            }
        });

        // Output tree
        jsonTree = new JTree(new DefaultMutableTreeNode("No data"));
        JScrollPane treeScroll = new JScrollPane(jsonTree);
        treeScroll.setBorder(BorderFactory.createTitledBorder("Parsed JSON Tree"));

        // Buttons panel
        JButton parseButton = new JButton("Parse");
        parseButton.addActionListener(e -> parseJson());

        JButton exportButton = new JButton("Export to .txt");
        exportButton.addActionListener(e -> exportParsedJson());

        statusLabel = new JLabel("Ready.");

        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        buttonPanel.add(parseButton);
        buttonPanel.add(exportButton);

        JPanel bottomPanel = new JPanel(new BorderLayout());
        bottomPanel.add(buttonPanel, BorderLayout.WEST);
        bottomPanel.add(statusLabel, BorderLayout.CENTER);

        // Layout
        JSplitPane splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, inputScroll, treeScroll);
        splitPane.setResizeWeight(0.5);

        add(splitPane, BorderLayout.CENTER);
        add(bottomPanel, BorderLayout.SOUTH);
    }

    private void openJsonFile() {
        JFileChooser chooser = new JFileChooser();
        chooser.setDialogTitle("Open JSON File");
        chooser.setFileFilter(new javax.swing.filechooser.FileNameExtensionFilter("JSON Files", "json"));
        int result = chooser.showOpenDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            loadJsonFromFile(chooser.getSelectedFile());
        }
    }

    private void loadJsonFromFile(File file) {
        try {
            String content = Files.readString(file.toPath());
            inputArea.setText(content);
            statusLabel.setText("Loaded: " + file.getName());
        } catch (IOException e) {
            showError("Failed to read file: " + e.getMessage());
        }
    }

    private void parseJson() {
        String jsonText = inputArea.getText();

        try {
            Tokenizer tokenizer = new Tokenizer(jsonText);
            List<Token> tokens = tokenizer.tokenize();

            JsonParser parser = new JsonParser(tokens);
            Object parsedJson = parser.parse();

            DefaultMutableTreeNode root = JsonTreeBuilder.buildTree(parsedJson);
            jsonTree.setModel(new javax.swing.tree.DefaultTreeModel(root));

            statusLabel.setText("Parsed successfully.");
        } catch (Exception e) {
            showError("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private void exportParsedJson() {
        try {
            String jsonText = inputArea.getText();
            Tokenizer tokenizer = new Tokenizer(jsonText);
            List<Token> tokens = tokenizer.tokenize();
            JsonParser parser = new JsonParser(tokens);
            Object parsedJson = parser.parse();

            String formatted = toJsonString(parsedJson, 0);

            JFileChooser chooser = new JFileChooser();
            chooser.setDialogTitle("Export Parsed JSON");
            chooser.setSelectedFile(new File("parsed_output.json"));
            int result = chooser.showSaveDialog(this);

            if (result == JFileChooser.APPROVE_OPTION) {
                Files.writeString(chooser.getSelectedFile().toPath(), formatted);
                statusLabel.setText("Exported to: " + chooser.getSelectedFile().getName());
            }

        } catch (Exception e) {
            showError("Export failed: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private String toJsonString(Object obj, int indent) {
        StringBuilder sb = new StringBuilder();
        String prefix = "  ".repeat(indent);

        if (obj instanceof Map<?, ?> map) {
            sb.append("{\n");
            int count = 0;
            for (var entry : map.entrySet()) {
                sb.append(prefix).append("  ")
                        .append("\"").append(entry.getKey()).append("\": ")
                        .append(toJsonString(entry.getValue(), indent + 1));
                if (++count < map.size()) sb.append(",");
                sb.append("\n");
            }
            sb.append(prefix).append("}");
        } else if (obj instanceof List<?> list) {
            sb.append("[\n");
            for (int i = 0; i < list.size(); i++) {
                sb.append(prefix).append("  ")
                        .append(toJsonString(list.get(i), indent + 1));
                if (i < list.size() - 1) sb.append(",");
                sb.append("\n");
            }
            sb.append(prefix).append("]");
        } else if (obj instanceof String str) {
            sb.append("\"").append(escapeString(str)).append("\"");
        } else {
            sb.append(String.valueOf(obj));
        }

        return sb.toString();
    }

    private String escapeString(String str) {
        return str.replace("\\", "\\\\")
                .replace("\"", "\\\"")
                .replace("\n", "\\n")
                .replace("\r", "\\r")
                .replace("\t", "\\t");
    }

    private void showError(String message) {
        statusLabel.setText(message);
        JOptionPane.showMessageDialog(this, message, "Error", JOptionPane.ERROR_MESSAGE);
    }

    public static void launch() {
        SwingUtilities.invokeLater(() -> new JsonParserGUI().setVisible(true));
    }
}
