package gui;

import javax.swing.tree.DefaultMutableTreeNode;
import java.util.*;

public class JsonTreeBuilder {
    public static DefaultMutableTreeNode buildTree(Object json) {
        return buildNode("root", json);
    }

    private static DefaultMutableTreeNode buildNode(String key, Object value) {
        DefaultMutableTreeNode node;

        if (value instanceof Map<?, ?> map) {
            node = new DefaultMutableTreeNode(key);
            for (Map.Entry<?, ?> entry : map.entrySet()) {
                node.add(buildNode(String.valueOf(entry.getKey()), entry.getValue()));
            }
        } else if (value instanceof List<?> list) {
            node = new DefaultMutableTreeNode(key);
            int index = 0;
            for (Object item : list) {
                node.add(buildNode("[" + index++ + "]", item));
            }
        } else {
            node = new DefaultMutableTreeNode(key + ": " + value);
        }

        return node;
    }
}
