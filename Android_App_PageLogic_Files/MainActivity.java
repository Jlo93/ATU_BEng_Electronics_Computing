package com.example.dataview;

import android.nfc.Tag;
import android.os.Bundle;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import com.google.android.material.tabs.TabLayout;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import android.os.TestLooperManager;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import android.view.View;

import android.view.Menu;
import android.view.MenuItem;

import org.w3c.dom.Text;

public class MainActivity extends AppCompatActivity {



    TextView CL001;
    TextView CL002;
    TextView Temp;
    TextView Perc;
    TextView TCTEFF;
    TextView LI001;
    TextView FL001;
    TextView FL004;
    TextView TU001;
    TextView pH;
    TextView doseratePred;
    TextView flowratePred;
    Button btn;
    DatabaseReference myRef;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);



        FloatingActionButton fab = findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();

            }
        });

    }
    //String CL001s = dataSnapshot.child("CL001").getValue().toString();
    //String CL002s = dataSnapshot.child("CL002").getValue().toString();
    //String Percs = dataSnapshot.child("Percentage").getValue().toString();
    //String Temps = dataSnapshot.child("Temp").getValue().toString();
    //String pHs = dataSnapshot.child("pH").getValue().toString();

    //String CL001s5 = CL001s.substring(0,Math.min(CL001s.length(),5));
    //String CL002s5 = CL002s.substring(0,Math.min(CL002s.length(),5));
    //String Percs5 = Percs.substring(0,Math.min(Percs.length(),5));
    //String Temps5 = Temps.substring(0,Math.min(Temps.length(),5));
    //String pHs5 = pHs.substring(0,Math.min(pHs.length(),5));

                //CL001.setText(CL001s5);
                //CL002.setText(CL002s5);
                //Perc.setText(Percs5);
                //Temp.setText(Temps5);
                //pH.setText(pHs5);

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}