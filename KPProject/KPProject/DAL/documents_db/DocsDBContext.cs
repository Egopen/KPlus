using System.Reflection.Metadata;
using KPProject.DAL.documents_db.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;

namespace KPProject.DAL.documents_db
{
    public class DocsDBContext:DbContext
    {
        public DbSet<Models.Document> Documents { get; set; } = null!;
        public DbSet<Models.DocumentContent> DocumentContents { get; set; } = null!;
        public DbSet<Models.Statistic> Statistics { get; set; } = null!;
        public DocsDBContext(DbContextOptions<DocsDBContext> options) : base(options)
        {
            Database.EnsureCreated();
        }
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseNpgsql(Environment.GetEnvironmentVariable("DOCSDBPATH"));
        }
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Models.Document>(entity =>
            {

                entity.Property(e => e.Created_at)
                      .HasDefaultValueSql("CURRENT_TIMESTAMP");

                entity.Property(e => e.Updated_at)
                      .HasDefaultValueSql("CURRENT_TIMESTAMP")
                      .ValueGeneratedOnAddOrUpdate();
            });
        }
    }
}
