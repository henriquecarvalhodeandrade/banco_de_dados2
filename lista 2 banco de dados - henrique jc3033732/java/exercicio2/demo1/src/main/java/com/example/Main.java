package com.example;

//package com.geeksforgeeks.application;

//import com.example.Cliente;
//import com.example.Endereco;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

public class Main {

    public static void main(String[] args)
    {

        // Create session factory
        SessionFactory factory
            = new Configuration()
                  .configure("hibernate.cfg.xml")
                  .addAnnotatedClass(Cliente.class)
                  .addAnnotatedClass(Endereco.class)
                  .buildSessionFactory();

        // Create session
        try (factory; Session session
                      = factory.getCurrentSession()) {
            // Get the current session

            // Create relevant object.
            Cliente cliente = new Cliente("RONALDO FENOMENO");

            Endereco endereco = new Endereco("Rua Velha", "117");

            endereco.setCliente(cliente);

            // Begin the transaction
            session.beginTransaction();

            // Save the Cliente object.
            // This will also save the Endereco
            // object as we have used CascadeType.ALL
            session.save(endereco);

            // Commit the transaction
            session.getTransaction().commit();

            System.out.println(
                "Transaction Successfully Completed!");
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }
}
