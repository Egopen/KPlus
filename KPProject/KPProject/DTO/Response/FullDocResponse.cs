using KPProject.DAL.documents_db.Models;
using System.ComponentModel.DataAnnotations;

namespace KPProject.DTO.Response
{
    public class FullDocResponse
    {
        public int Id { get; set; }
        public string Title { get; set; }

        public string Content {  get; set; }

    }
}
