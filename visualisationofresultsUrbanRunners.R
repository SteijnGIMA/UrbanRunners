library(ggplot2)
library("readxl")

setwd('C:/Users/michi/Documents/GIMA/Module 6')
table = read_excel("Final_routestats.xlsx", sheet = 'routestats_Amsterdam')

#UHI
ggplot(
  data = table, 
  mapping = aes(x=((RR_length - SR_length) / SR_length)*100, y=((RR_UHI - SR_UHI) / SR_UHI)*100)) + 
    geom_point() + theme_bw() + xlab("Relative increase in length (in %)") + ylab('Relative change in UHI (in %)') + ggtitle('Rachid Route vs Shortest Route')  + ylim(-100,50)

ggplot(
  data = table, 
  mapping = aes(x=((WR_length - SR_length) / SR_length)*100, y=((WR_UHI - SR_UHI) / SR_UHI)*100)) + 
  geom_point() + theme_bw() + xlab("Relative increase in length (in %)") + ylab('Relative change in UHI (in %)') + ggtitle('Willemijn Route vs Shortest Route')  + ylim(-100, 50)
#greenspaces
ggplot(
  data = table, 
  mapping = aes(x=((RR_length - SR_length) / SR_length)*100, y=((RR_greenspace - SR_greenspace) / SR_greenspace)*100)) + 
  geom_point() + theme_bw() + xlab("Relative increase in length (in %)") + ylab('Relative increase in greenspaces (in %)') + ggtitle('Rachid Route vs Shortest Route') + ylim(-1, 2000) + xlim(-1, 50)

ggplot(
  data = table,
  mapping = aes(x=((WR_length - SR_length) / SR_length)*100, y=((WR_greenspace - SR_greenspace) / SR_greenspace)*100)) +
  geom_point() + theme_bw() + xlab("Relative increase in length (in %)") + ylab('Relative increase in greenspaces (in %)') + ggtitle('Willemijn Route vs Shortest Route') + ylim(-1, 2000) + xlim(-1, 50)

#grade
ggplot(
  data = table,
  mapping = aes(x=((WR_length - SR_length) / SR_length)*100, y=((WR_grade - SR_grade) / SR_grade)*100)) +
  geom_point() + theme_bw() + xlab("Relative increase in length (in %)") + ylab('Relative change in slope (in %)') + ggtitle('Willemijn Route vs Shortest Route') + ylim(-100, 1000)

#traffic signals
ggplot(
  data = table, 
  mapping = aes(x=(RR_length - SR_length), y=(RR_trafficsignals - SR_trafficsignals))) + 
  geom_point() + theme_bw() + xlab("Increase in length") + ylab('Change in traffic signal occurance') + ggtitle('Rachid Route vs Shortest Route')

ggplot(
  data = table, 
  mapping = aes(x=(RR_length - SR_length), y=(WR_trafficsignals - SR_trafficsignals))) + 
  geom_point() + theme_bw() + xlab("Increase in length") + ylab('Change in traffic signal occurance') + ggtitle('Willemijn Route vs Shortest Route')

#waterpoints
ggplot(
  data = table, 
  mapping = aes(x=(RR_length - SR_length), y=(RR_waterpoints - SR_waterpoints))) + 
  geom_point() + theme_bw() + xlab("Increase in length") + ylab('Change in waterpoint occurance') + ggtitle('Rachid Route vs Shortest Route')

#surface
ggplot(
  data = table, 
  mapping = aes(x=((RR_length - SR_length) / SR_length)*100, y=((RR_prefunpaved)*100))) + 
  geom_point() + theme_bw() + xlab("Relative increase in length (in %)") + ylab('Average unpaved surface (in %)') + ggtitle('Rachid Route vs Shortest Route') + ylim(-1, 100) + xlim(-1, 150)

ggplot(
  data = table,
  mapping = aes(x=((WR_length - SR_length) / SR_length)*100, y=((WR_prefpaved)*100))) +
  geom_point() + theme_bw() + xlab("Relative increase in length (in %)") + ylab('Relative paved surface (in %)') + ggtitle('Willemijn Route vs Shortest Route') + ylim(-1, 100) + xlim(-1, 150)