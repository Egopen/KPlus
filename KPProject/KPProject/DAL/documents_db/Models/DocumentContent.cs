using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace KPProject.DAL.documents_db.Models
{
    [Table("document_contents")]
    public class DocumentContent
    {
        [Column("id")]
        public int Id { get; set; }
        [Column("content"),Required]
        public string Content { get; set; }
        [Column("document_id")]
        public int DocumentId {  get; set; }
        public Document? Document { get; set; }


    }
}
