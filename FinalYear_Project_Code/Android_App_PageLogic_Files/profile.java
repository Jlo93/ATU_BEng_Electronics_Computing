package com.example.dataview;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import org.w3c.dom.Text;

import static com.example.dataview.R.id.CL001id_;
import static com.example.dataview.R.id.Tempid_;
import static com.example.dataview.R.id.pHid_;

public class profile extends AppCompatActivity {

    private FirebaseUser user;
    private DatabaseReference reference;
    private DatabaseReference myRef;
    private DatabaseReference MLOutRef;

    private String userID;
    private Button logout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);


        logout = (Button)findViewById(R.id.logOut);
        logout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                FirebaseAuth.getInstance().signOut();
                startActivity(new Intent(profile.this,Auth.class));
            }
        });

        // get current users information
        user = FirebaseAuth.getInstance().getCurrentUser();
        // set up firebase reference with the path aiming at the user tab
        reference = FirebaseDatabase.getInstance().getReference("Users");
        userID = user.getUid();

        //link the textviews
        final TextView pHTextView = (TextView)findViewById(R.id.pHid_);
        final TextView TempTextView = (TextView)findViewById(R.id.Tempid_);
        final TextView tu001TextView = (TextView)findViewById(R.id.TU001id_);
        final TextView fl001TextView = (TextView)findViewById(R.id.FL001id_);
        final TextView cl001TextView = (TextView)findViewById(CL001id_);
        final TextView li001TextView = (TextView)findViewById(R.id.LI001id_);
        final TextView cl002TextView = (TextView)findViewById(R.id.CL002id_);
        final TextView fl004TextView = (TextView)findViewById(R.id.FL004id_);
        final TextView MLTextView = (TextView)findViewById(R.id.MLid_);

        final TextView greetingTextView = (TextView)findViewById(R.id.greeting);
        final TextView fullNameTextView = (TextView)findViewById(R.id.fullName);
        final TextView emailTextView = (TextView)findViewById(R.id.emailAddress);
        final TextView plantTextView = (TextView)findViewById(R.id.plant);

        reference.child(userID).addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                User userProfile = snapshot.getValue(User.class);

                if(userProfile != null){
                    String fullName = userProfile.fullName;
                    String email = userProfile.email;
                    String plant = userProfile.plant;

                    greetingTextView.setText("Welcome, "+ fullName + "!");
                    fullNameTextView.setText(fullName);
                    emailTextView.setText(email);
                    plantTextView.setText(plant);
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {
                Toast.makeText(profile.this,"Something went wrong",Toast.LENGTH_LONG).show();
            }
        });

        MLOutRef = FirebaseDatabase.getInstance().getReference().child("Data").child("ML Data & SMS Alarm Setpoints");
        MLOutRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                String pred1s = snapshot.child("ML Suggested Control Set-Point (ML Model Output)").getValue().toString();
                String pred1s5 = pred1s.substring(0,Math.min(pred1s.length(),4));
                MLTextView.setText(pred1s5);
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });

        myRef = FirebaseDatabase.getInstance().getReference().child("Data").child("Process Variables (ML Model Inputs)");
        myRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot datasnapshot) {

                String CL001s = datasnapshot.child("Cl Res CL001").getValue().toString();
                String CL002s = datasnapshot.child("Cl Val CL002").getValue().toString();
                //String TCTEFFs = datasnapshot.child("Contact Time(TCTEFF)").getValue().toString();
                String Temps = datasnapshot.child("Temp").getValue().toString();
                String pHs = datasnapshot.child("pH").getValue().toString();
                String LI001s = datasnapshot.child("Reservoir Level LI001").getValue().toString();
                String FL001s = datasnapshot.child("Inflow FL001").getValue().toString();
                String FL004s = datasnapshot.child("Outlet Flow FL004").getValue().toString();
                String TU001s = datasnapshot.child("Turbidity TU001").getValue().toString();
                //String pred1s = datasnapshot.child("AI Suggested SP23 Prediction").getValue().toString();
                //String pred2s = datasnapshot.child("Clflow rate Prediction").getValue().toString();


                String CL001s5 = CL001s.substring(0,Math.min(CL001s.length(),4));
                String CL002s5 = CL002s.substring(0,Math.min(CL002s.length(),4));
                //String TCTEFFs5 = TCTEFFs.substring(0,Math.min(TCTEFFs.length(),5));
                String Temps5 = Temps.substring(0,Math.min(Temps.length(),4));
                String pHs5 = pHs.substring(0,Math.min(pHs.length(),4));
                String LI001s5 = LI001s.substring(0,Math.min(LI001s.length(),4));
                String FL001s5 = FL001s.substring(0,Math.min(FL001s.length(),4));
                String FL004s5 = FL004s.substring(0,Math.min(FL004s.length(),4));
                String TU001s5 = TU001s.substring(0,Math.min(TU001s.length(),6));
                //String pred1s5 = pred1s.substring(0,Math.min(pred1s.length(),4));
                //String pred2s5 = pred2s.substring(0,Math.min(pred2s.length(),5)

                cl001TextView.setText(CL001s5);
                cl002TextView.setText(CL002s5);
                TempTextView.setText(Temps5);
                pHTextView.setText(pHs5);
                li001TextView.setText(LI001s5);
                fl001TextView.setText(FL001s5);
                fl004TextView.setText(FL004s5);
                tu001TextView.setText(TU001s5);
               // MLTextView.setText(pred1s5);
                
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });



    }
}


