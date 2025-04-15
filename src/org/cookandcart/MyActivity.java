package org.cookandcart.cookandcart;

import org.qtproject.qt5.android.bindings.QtActivity;
import android.util.Log;

public class MyActivity extends QtActivity {
    private static final String TAG = "MyActivity";

    @Override
    public void onBackPressed() {
        // Do nothing (or add your own logic) to disable the default behavior.
        Log.d(TAG, "onBackPressed() intercepted; not calling super.");
    }
}
