using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace KPProject.DAL.documents_db.Models
{
    [Table("documents")]
    public class Document
    {
        [Column("id")]
        public int Id { get; set; }
        [Column("title"), Required]
        public string Title { get; set; }
        [Column("doc_type"),Required]
        public string Doc_type { get; set; }
        [Column("created_at")]
        public DateTime Created_at { get; set; }

        [Column("updated_at")]
        public DateTime Updated_at { get; set; }

        public DocumentContent? DocumentContent { get; set; }

    }
}
