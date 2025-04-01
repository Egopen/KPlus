using System.ComponentModel.DataAnnotations;
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;


[Table("stats_db")] 
public class Stats :BaseModel
{
    [PrimaryKey("id", false)]
    public int Id { get; set; }

    [Column("created_at"),Required]
    public DateTime CreatedAt { get; set; }

    [Column("stat_name"), Required]
    public string StatName { get; set; }

    [Column("count"), Required]
    public int Count { get; set; }
}
