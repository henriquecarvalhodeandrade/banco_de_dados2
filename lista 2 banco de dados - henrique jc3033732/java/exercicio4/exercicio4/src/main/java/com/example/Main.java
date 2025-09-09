package com.example;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

public class Main {
    public static void main(String[] args) {
        SessionFactory factory
            = new Configuration()
                  .configure("hibernate.cfg.xml")
                  .addAnnotatedClass(Item.class)
                  .addAnnotatedClass(Pedido.class)
                  .buildSessionFactory();

       Session session = factory.getCurrentSession();
 
        session.beginTransaction();
 
        Pedido pedido1 = new Pedido("08-09-2025", 229.99);
        Pedido pedido2 = new Pedido("08-10-2025", 369.99);
 
        Item item1 = new Item("AirFryer", 229.99);
        Item item2 = new Item("Makita", 109.99);
        Item item3 = new Item("Trena", 49.99);
 
        pedido1.getItens().add(item1);
        pedido1.getItens().add(item2);
 
        pedido2.getItens().add(item1);
        pedido2.getItens().add(item2);
        pedido2.getItens().add(item3);
 
        item1.getPedidos().add(pedido1);
        item1.getPedidos().add(pedido2);
 
        item2.getPedidos().add(pedido1);
        item2.getPedidos().add(pedido2);
 
        item3.getPedidos().add(pedido2);
 
        session.save(pedido1);
        session.save(pedido2);
 
        session.getTransaction().commit();
        System.out.println("Great! Pedidos were saved");
    }
}