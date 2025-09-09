package com.example;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;

@Entity
@Table(name = "endereco")
public class Endereco {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private int id;

    @Column(name = "rua") private String rua;

    @Column(name = "numero")
    private String numero;

    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "cliente_id")
    private Cliente cliente;

    public Endereco() {}

    public Endereco(String rua, String numero)
    {
        this.rua = rua;
        this.numero = numero;
    }

    public int getId() { return id; }

    public void setId(int id) { this.id = id; }

    public String getRua() { return rua; }

    public void setRua(String rua)
    {
        this.rua = rua;
    }

    public String getNumero()
    {
        return numero;
    }

    public void
    setNumero(String numero)
    {
        this.numero = numero;
    }

    public Cliente getCliente() {return this.cliente;}

    public void setCliente(Cliente cliente) {this.cliente = cliente;}

    @Override public String toString()
    {
        return "StudentGfgDetail{"
            + "id=" + id + ", rua='" + rua + '\''
            + ", numero=" + numero
            + '}';
    }
}
