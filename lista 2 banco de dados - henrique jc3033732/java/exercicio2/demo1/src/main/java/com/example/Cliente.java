package com.example;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "cliente")
public class Cliente {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private int id;

    @Column(name = "nome") private String nome;

    public Cliente() {}

    public Cliente(String nome) {this.nome = nome;}

    public int getId() { return id; }

    public void setId(int id) { this.id = id; }

    public String getNome() { return this.nome; }

    public void setNome(String nome)
    {
        this.nome = nome;
    }

    @Override public String toString()
    {
        return "Cliente{"
            + "id=" + id + ", nome='" + this.nome
            + '}';
    }
}
