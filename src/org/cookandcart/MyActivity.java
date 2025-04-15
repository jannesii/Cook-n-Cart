package org.cookandcart.cookandcart;

import org.qtproject.qt5.android.bindings.QtActivity;
import android.widget.Toast;

public class MyActivity extends QtActivity {
    @Override
    public void onBackPressed() {
        console.log("Back button pressed, but doing nothing.");
        // Do nothing; override to disable default behavior.
        // You could add a log here or your own custom behavior if needed.
        // For example, if you want to dismiss a keyboard or do some other logic, do it here.
        // If you really want to completely disable the back press, just leave it empty.
    }
}
