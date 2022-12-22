#Observations of activity aggregated at the level of different administrative entities

BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX myc: <https://elections.ontotext.com/resource/prop/cube/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
PREFIX qb: <http://purl.org/linked-data/cube#>
PREFIX party: <https://elections.ontotext.com/resource/party/>
insert {
  graph <graph/cube/ath_pi_activity> {
  ?ACT_URI a qb:Observation , myc:Activity ;
             qb:dataSet <cube/activity> ;
             myc:election ?election ;
             myc:locality ?locality ;
             myc:local_election ?local_election ;
             myc:voters ?VOTERS ;
             myc:voted ?VOTED ;
  .
  }
} where {
    {
        select ?locality ?election ?local_election (sum(?voters) as ?VOTERS) (sum(?voted) as ?VOTED) where {
            {
                ?voting a my:Voting ;
                        myd:section/myd:place/myd:municipality?/myd:mir? ?locality
            }
            union
            {
                ?voting a my:Voting ;
                        myd:election/myd:jurisdiction ?locality ;
                                    myd:section/myd:place/myd:municipality jurisdiction:2246.
            } union
            {
                ?voting a my:Voting ;
                        myd:election/myd:jurisdiction ?locality .
                filter(sameterm(?locality,jurisdiction:32))
            }
            ?voting myd:main_election ?election;
                    myd:election ?local_election ;
                    myd:voters_voted_count ?voted ;
                    myd:voters_count ?voters ;
                    .
            ?election myd:type ?type .
            filter (?type in ("parliamentary"))
        } group by ?locality ?election ?local_election
    }
    bind(uri(concat("cube/activity/",str(sha1(concat(str(?locality),str(?election)))))) as ?ACT_URI)
}