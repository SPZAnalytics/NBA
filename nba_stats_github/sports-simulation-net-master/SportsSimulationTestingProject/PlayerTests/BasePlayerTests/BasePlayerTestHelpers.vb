Option Strict On

Imports SportsSimulation.Player.Base

Namespace PlayerTests
    Namespace Base

        Public Class BasePlayerTestHelpers

            Public Property Ids As List(Of BasePlayerId)
            Public Property Stats As Dictionary(Of String, Object)
            Public Property Year As Integer

            Public Sub New()
                Me.Ids = New List(Of BasePlayerId) From {
                        {New BasePlayerId("ABDULKA01", "basketball-reference.com")},
                        {New BasePlayerId("ALLENRA01", "basketball-reference.com")},
                        {New BasePlayerId("DENGLU01", "basketball-reference.com")}
                    }
                Me.Stats = New Dictionary(Of String, Object) From {
                    {"Minutes", 2010},
                    {"Games", 40},
                    {"Points", 2010},
                    {"Rebounds", 201}}
                Me.Year = 2010
            End Sub

            Public Function CreateAlteredStats() As Dictionary(Of String, Object)
                Dim stats As New Dictionary(Of String, Object)
                Dim r As New Random
                stats("Games") = Me.Stats("Games")
                stats("Points") = CInt(CInt(Me.Stats("Points")) * r.NextDouble)
                stats("Minutes") = CInt(CInt(Me.Stats("Minutes")) * r.NextDouble)
                stats("Rebounds") = CInt(CInt(Me.Stats("Rebounds")) * r.NextDouble)
                Return stats
            End Function

            Public Function CreateId() As BasePlayerId
                Return Me.Ids(0)
            End Function

            Public Function CreateIds() As List(Of BasePlayerId)
                Return Me.Ids
            End Function

            Public Function CreatePlayerWithStats() As BasePlayer
                Dim player As New BasePlayer
                player.AddSeason(Me.CreateSeasonWithStats(Me.Year))
                Return player
            End Function

            Public Function CreatePlayersWithStats() As List(Of BasePlayer)
                Dim players As New List(Of BasePlayer)
                For Each id As BasePlayerId In Me.Ids
                    Dim player As New BasePlayer
                    player.AddId(id)
                    player.AddSeason(Me.CreateSeasonWithStats(Me.Year - 1))
                    player.AddSeason(Me.CreateSeasonWithStats(Me.Year))
                    players.Add(player)
                Next
                Return players
            End Function

            Public Function CreateSeason(ByVal year As Integer) As BasePlayerSeason
                Dim season As New BasePlayerSeason(year)
                Return season
            End Function

            Public Function CreateSeasonWithStats(ByVal year As Integer) As BasePlayerSeason
                Dim season As New BasePlayerSeason(year)
                Dim teamSeasons As New List(Of BasePlayerTeamSeason) From {
                    {New BasePlayerTeamSeason(year, Me.Stats)},
                    {New BasePlayerTeamSeason(year, Me.Stats)}
                }
                season.AddPlayerTeamSeasons(teamSeasons)
                Return season
            End Function

            Public Function CreateSeasons() As List(Of BasePlayerSeason)
                Dim season As New List(Of BasePlayerSeason)
                Return season
            End Function

            Public Function CreateSeasonsWithStats() As List(Of BasePlayerSeason)
                Dim seasons As New List(Of BasePlayerSeason)
                Dim season As New BasePlayerSeason(Me.Year - 1)
                Dim playerTeamSeasons As New List(Of BasePlayerTeamSeason) From {
                    {New BasePlayerTeamSeason(Me.Year - 1, Me.Stats)},
                    {New BasePlayerTeamSeason(Me.Year - 1, Me.Stats)}
                }
                season.AddPlayerTeamSeasons(playerTeamSeasons)
                seasons.Add(season)
                season = New BasePlayerSeason(Me.Year)
                playerTeamSeasons = New List(Of BasePlayerTeamSeason) From {
                    {New BasePlayerTeamSeason(Me.Year, Me.Stats)},
                    {New BasePlayerTeamSeason(Me.Year, Me.Stats)}
                }
                season.AddPlayerTeamSeasons(playerTeamSeasons)
                seasons.Add(season)
                Return seasons
            End Function

            ' private methods

        End Class
    End Namespace
End Namespace
