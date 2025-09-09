package com.example;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

public class Main {
    public static void main(String[] args) {
        System.out.println(".......Hibernate One To Many Mapping Example.......\n");
        
        SessionFactory factory
       = new Configuration()
             .configure("hibernate.cfg.xml")
             .addAnnotatedClass(Cliente.class)
             .addAnnotatedClass(Pedido.class)
             .buildSessionFactory();

        Session session = factory.getCurrentSession();

        try{
            session.beginTransaction();
 
            Cliente cliente = new Cliente("IRAN FERREIRA");
            session.save(cliente);
 
            Pedido pedido1 = new Pedido("08-09-2025", 200.76);  
            pedido1.setCliente(cliente);  
            session.save(pedido1);
 
            Pedido pedido2 = new Pedido("17-10-2025", 176.34);  
            pedido2.setCliente(cliente);
            session.save(pedido2);
 
            Pedido pedido3 = new Pedido("11-11-2025", 579.99);  
            pedido3.setCliente(cliente);
            session.save(pedido3);
 
            // Committing The Transactions To The Database
            session.getTransaction().commit();
 
            System.out.println("\n.......Records Saved Successfully To The Database.......");
        } catch(Exception sqlException) {
            if(null != session.getTransaction()) {
                System.out.println("\n.......Transaction Is Being Rolled Back.......");
                session.getTransaction().rollback();
            }
            sqlException.printStackTrace();
        } finally {
            if(session != null) {
                session.close();
            }
        }
    }
}