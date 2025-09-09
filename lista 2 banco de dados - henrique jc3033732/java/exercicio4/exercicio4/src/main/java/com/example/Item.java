package com.example;

import java.util.Set;
import java.util.HashSet;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.ManyToMany;
import javax.persistence.Table;



@Entity
@Table(name = "item")
public class Item implements java.io.Serializable{
    
    private int id;
    
    private String tipo;
    
    private double preco;
    
    private Set<Pedido> pedidos = new HashSet<Pedido>(0);
    
    public Item () {}
    public Item (String tipo, double preco) {
        this.tipo = tipo;
        this.preco = preco;
    }
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    public int getId() {
        return id;
    }
    
    public void setId(int id) {
        this.id = id;
    }
    
    @Column(name = "tipo")
    public String getTipo() {
        return tipo;
    }
    
    public void setTipo(String tipo) {
        this.tipo = tipo;
    }
    
    @Column(name = "preco")
    public double getPreco() {
        return preco;
    }
    
    public void setPreco(double preco) {
        this.preco = preco;
    }
    
    @ManyToMany(fetch = FetchType.LAZY, mappedBy = "itens")
    public Set<Pedido> getPedidos() {
        return pedidos;
    }
    
    public void setPedidos(Set<Pedido> pedidos) {
        this.pedidos = pedidos;
    }
    
    private static final long serialVersionUID = 1L;
}
