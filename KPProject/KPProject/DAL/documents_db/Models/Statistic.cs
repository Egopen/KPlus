using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace KPProject.DAL.documents_db.Models
{
    [Table("statistics")]
    public class Statistic
    {
        [Column("id")]
        public int Id { get; set; }
        [Column("visited_count")]
        public int VisitedCount { get; set; }
        [Column("avr_time"),Required]
        public int AvrTime { get; set; }
        [Column("document_id"),Required]
        public int DocumentId { get; set; }
        public Document? Document { get; set; }

    }
}
